import xml.etree.ElementTree as ET
import pandas as pd
from pyvis.network import Network
import os 

# Parse the file
file_path = r"<path of your .twb file>"

def Tableau_Calculation_Dependencies(file_path,root):
    folder_path = os.path.dirname(file_path)

    # Create a new directory called 'shapes' in the same directory as xml_file_path
    output_dir = os.path.join(folder_path, 'Calculation Dependency Analysis')
    os.makedirs(output_dir, exist_ok=True)

    # Find the <datasources> element that is a direct child of <workbook>, because the <datasources> element will also apear under the table/ view
    datasources_element = None
    for child in root:
        if child.tag == 'datasources':
            datasources_element = child
            break

    # Extracting the <column> & group elements
    columns = []
    groups = []
    group_set = set()

    if datasources_element is not None:
        for datasource in datasources_element.findall('datasource'):
            for column in datasource.findall('column'):
                col_info = {
                    "datasource": datasource.get('caption'),
                    "underlying_name": column.get('name'),
                    "presented_name": column.get('caption'),
                    "datatype": column.get('datatype'),
                    "role": column.get('role'),
                    "type": column.get('type'),
                    "class": None,
                    "underlying_formula": None
                }

                # If Datasource is parameter then use 'name' attribute instead of 'caption' 
                if datasource.get('name') == 'Parameters':
                    col_info["datasource"] = datasource.get('name')
                    
                # Check if there is a <calculation> child element
                calculation = column.find('calculation')
                if calculation is not None:
                    col_info["class"] = calculation.get('class')
                    col_info["underlying_formula"] = calculation.get('formula')
                
                # Classify the column
                if column.get('param-domain-type') is not None:
                    col_info["classification"] = "parameter"
                elif calculation is not None:
                    col_info["classification"] = "calculation field"
                else:
                    col_info["classification"] = "sourced"
                
                columns.append(col_info)

                # if presented_name is none, get from Underlyiny name
                if col_info["presented_name"] is None:
                    col_info["presented_name"] = col_info["underlying_name"].strip('[]')
        
        #extract the set in <group> tag
        for group in datasource.findall('group'):
            if group.get('{http://www.tableausoftware.com/xml/user}ui-builder') == 'filter-group':
                groupfilter = group.find('groupfilter')
                if groupfilter is not None:  # the set may mark source field as member or level
                    underlying_formula = groupfilter.get("member") 
                    if underlying_formula is None:
                        underlying_formula = groupfilter.get("level")
                    
                    group_key = (group.get('caption'), group.get('name'))  # Use a tuple to represent the unique key
                    if group_key not in group_set:
                        group_set.add(group_key)
                        group_info = {
                            "type": "group",
                            "datasource": datasource.get('caption'),
                            "underlying_name": group.get('name'),
                            "presented_name": group.get('caption'),
                            "datatype": "set",
                            "underlying_formula": underlying_formula,
                            "classification": "calculation field"
                        }
                groups.append(group_info)
                
    columns_df = pd.DataFrame(columns)
    groups_df = pd.DataFrame(groups)

    combined_df = pd.concat([columns_df,groups_df]).reset_index(drop=True)
    combined_df = combined_df.fillna('')
    # combined_df
    ##### replacing underlying_name with presented_name in the underlying_formula
    # Create a mapping from Underlying Name to Presented Name
    mapping = dict(zip(combined_df['underlying_name'], combined_df['presented_name']))

    # Function to replace underlying names in the formula with presented names
    def update_formula(formula, mapping):
        for underlying_name, presented_name in mapping.items():
            # Remove brackets from underlying_name for replacement
            clean_name = underlying_name.strip('[]')
            # Replace all instances of the underlying name in the formula
            formula = formula.replace(clean_name, presented_name)
        return formula

    # Apply the function to create a new column 'New Formula'
    combined_df['presented_formula'] = combined_df['underlying_formula'].apply(lambda x: update_formula(x, mapping))

    #see if a df contains comment
    def contains_comment(row):
        if row['classification'] != 'calculation field':
            return None
        elif '//' in row['presented_formula']:
            return True
        return False  # Default case if neither condition is met

    # Add the new column based on the function
    combined_df['comment_exist'] = combined_df.apply(contains_comment, axis=1)


    # Output the csv
    output_csv_name = r"field_list.csv"
    output_csv_path = os.path.join(output_dir,output_csv_name)
    combined_df.to_csv(output_csv_path)
    print(f"\n    csv file containing the field info saved to {output_csv_path}\n")

    # Get unique datasource values and remove 'Parameters'
    datasources = [source for source in combined_df['datasource'].unique() if source != 'Parameters']
    df_param = combined_df[combined_df['datasource'] == 'Parameters']

    # Define the color map for classifications
    color_map = {
        'parameter': '#936eb0',
        'sourced': 'green',
        'calculation field': '#f38c5f'
    }

    def generate_stats_html(df_filtered, source, color_map):
        stats_html = f"<h3>Workbook: {file_path}</h3>"
        stats_html += f"<h5>Statistics for datasource: {source}</h5>"
        stats_html += "<ul>"
        classification_counts = df_filtered['classification'].value_counts().to_dict()
        for classification, count in classification_counts.items():
            color = color_map.get(classification, 'black')  # Default to black if classification not in color_map
            stats_html += f"<li style='color: {color};'>{classification}: {count}</li>"
        stats_html += "</ul>"

        # Adding the additional lines of text at the end
        stats_html += """
        <p>    Noted that these graphs are not suitable for determining if the fields are redundant, 
        since independent fields could be used for actions and sheets.</p>
        <p>    The best use of this graph is to:
        <ul>
            <li> keep track of the interconnectivity between fields</li>
            <li> estimate what would be impacted when a field is subjected to change</li>
            <li> identify main groups of calculations as node clusters </li>
            <li> see the formula of the calculation field without opening each field.</li>
        </ul>
        </p>
        """
        
        return stats_html

    # Generate one file for each data source
    for source in datasources:
        
        # Create a Network
        net = Network(notebook=True, cdn_resources='remote',height='750px', width='100%',select_menu=True,filter_menu=True,directed=True)
        # net.show_buttons(filter_=['physics']) # doesn't work if set_options is used
        
        net.set_options("""
            const options = {
            "physics": {
                "enabled": true,
                "forceAtlas2Based": {
                "springLength": 100
                },
                "minVelocity": 0.75,
                "solver": "forceAtlas2Based"
            }
        }""")   

        # Filter the DataFrame by the current datasource
        df_filtered = combined_df[combined_df['datasource'] == source]
        df_filtered = pd.concat([df_filtered, df_param])

        # Initialize a dictionary to keep track of node degrees
        node_degrees = {row['presented_name']: 0 for _, row in df_filtered.iterrows()}

        # Add nodes
        for _, row in df_filtered.iterrows():
            node_info = (
                f"Name: {row['presented_name']}\n"
                f"Datatype: {row['datatype']}\n"
                f"Type: {row['type']}\n"
                f"Classification: {row['classification']}\n"
                f"Datasource: {row['datasource']}\n\n"
            )

            if row['presented_formula']:
                node_info += (
                    f"Formula:\n"
                    f"{row['presented_formula']}"
                )
            # Assign a color based on the classification
            node_color = color_map.get(row['classification'], 'lightgray')
            net.add_node(row['presented_name'], label=row['presented_name'], title=node_info, color=node_color)
            
        # Add edges with arrows and count node degrees
        for _, row in df_filtered.iterrows():
            for _, row_target in df_filtered.iterrows():
                if row['underlying_name'] in row_target['underlying_formula']:
                    net.add_edge(row['presented_name'], row_target['presented_name'], arrows='to')
                    node_degrees[row['presented_name']] += 1
                    node_degrees[row_target['presented_name']] += 1
    
        
        # Calculate the maximum node degree and update node sizes
        max_degree = max(node_degrees.values(), default=1)  # Ensure max_degree is at least 1 to avoid ZeroDivisionError
        for node_id, degree in node_degrees.items():
            # Use default size if all degrees are zero
            size = 10 if max_degree == 0 else 10 + (degree / max_degree) * 30
            net.get_node(node_id)['size'] = size

    ####### Add HTML header
        # Generate statistics HTML
        stats_html = generate_stats_html(df_filtered, source, color_map)
        
        # Save to HTML file
        output_html_name = f'network_{source}.html'
        output_html_path = os.path.join(output_dir,output_html_name)
        net.write_html(output_html_path)

        # Read the existing HTML content
        with open(output_html_path, 'r') as f:
            content = f.read()

        # Insert the statistics HTML at the top of the body
        content = content.replace('<body>', f'<body>{stats_html}', 1)

        # Write the modified content back to the file
        with open(output_html_path, 'w') as f:
            f.write(content)

        print(f"    Network graph for datasource '{source}' saved to {output_html_path}\n")

if __name__ == '__main__':
    print('text')
    tree = ET.parse(file_path)
    root = tree.getroot()
    Tableau_Calculation_Dependencies(file_path,root)