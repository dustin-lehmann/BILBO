from dataclasses import dataclass, fields, is_dataclass
from typing import Type, Any
import graphviz


def analyze_dataclass(
        dataclass_type: Type[Any],
        print_to_terminal: bool = False,
        print_to_file: bool = True,
        generate_figure: bool = False,
):
    """
    Generates diagnostics for a dataclass, including its fields and nested structures.
    Ensures unique nodes for fields with the same name and prevents parents from linking to grandchildren.

    :param dataclass_type: The dataclass type to process.
    :param print_to_terminal: If True, prints the field paths to the terminal.
    :param print_to_file: If True, writes the field paths to a .txt file named after the dataclass.
    :param generate_figure: If True, generates a tree diagram named after the dataclass.
    """
    if not is_dataclass(dataclass_type):
        raise ValueError("The provided type is not a dataclass.")

    # Define color mapping for types
    type_colors = {
        "dataclass": "lightblue",
        "float": "lightgreen",
        "int": "lightcoral",
        "str": "wheat",
        "List": "yellow",
        "Dict": "pink",
        "Optional": "gray",
    }

    def get_color(field_type):
        """Get the color for a field type."""
        if hasattr(field_type, "__origin__"):  # Handle typing constructs (e.g., List, Dict, Optional)
            origin = field_type.__origin__.__name__
            return type_colors.get(origin, "white")
        if is_dataclass(field_type):  # Handle dataclasses
            return type_colors["dataclass"]
        return type_colors.get(field_type.__name__, "white")  # Default to white if no match

    def get_field_paths_and_structure(data_type, prefix=""):
        """Recursively extracts fields and nested dataclasses."""
        paths = []
        structure = []
        for field in fields(data_type):
            field_name = field.name
            field_type = field.type
            full_path = f"{prefix}{field_name}"

            paths.append(full_path)  # Add current field's path
            structure.append((prefix, field_name, field_type, is_dataclass(field_type)))

            # If the field type is another dataclass, process it recursively
            if is_dataclass(field_type):
                nested_paths, nested_structure = get_field_paths_and_structure(field_type, prefix=f"{full_path}.")
                paths.extend(nested_paths)
                structure.extend(nested_structure)
        return paths, structure

    # Generate field paths and structure
    all_paths, structure = get_field_paths_and_structure(dataclass_type)

    # Write the paths to the output file if enabled
    dataclass_name = dataclass_type.__name__
    if print_to_file:
        txt_file_name = f"{dataclass_name}.txt"
        with open(txt_file_name, "w") as file:
            file.write(f"Fields and Paths for Dataclass: {dataclass_name}\n")
            for path in all_paths:
                file.write(f"{path}\n")

    # Optionally print paths to terminal
    if print_to_terminal:
        print(f"Fields and Paths for Dataclass: {dataclass_name}")
        for path in all_paths:
            print(path)

    # Optionally generate a tree diagram
    if generate_figure:
        graph = graphviz.Digraph(format="png")
        graph.attr(rankdir="TB")  # Top-to-Bottom layout
        graph.attr("node", shape="box")

        # Add the root node for the dataclass
        root_name = dataclass_type.__name__
        graph.node(root_name, f"{root_name} (dataclass)", style="filled", fillcolor=type_colors["dataclass"])

        # Recursive function to add nodes and edges
        def add_to_graph(parent, current_prefix, structure):
            for prefix, field_name, field_type, is_nested in structure:
                # Only connect immediate children to the current parent
                if prefix.rstrip(".") == current_prefix.rstrip("."):
                    # Create a globally unique node ID using the full path
                    node_id = f"{prefix}{field_name}".replace(".", "_")
                    node_label = f"{field_name} ({field_type.__name__})" if not is_nested else field_name
                    color = get_color(field_type)

                    # Add the node to the graph
                    graph.node(node_id, node_label, style="filled", fillcolor=color)
                    graph.edge(parent, node_id)

                    # Recursively add nested dataclass children
                    if is_nested:
                        nested_structure = [
                            item for item in structure if item[0].startswith(f"{prefix}{field_name}.")
                        ]
                        add_to_graph(node_id, f"{prefix}{field_name}.", nested_structure)

        # Start adding nodes from the root
        add_to_graph(root_name, "", structure)

        # Render the figure with the name of the dataclass
        graph.render(dataclass_name, cleanup=True)