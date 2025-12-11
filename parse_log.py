import json


def parse_log(log_file):
    with open(log_file, 'r') as f:
        log = f.read()
    log_json = json.loads(log)
    return log_json


def get_violations(result_dict):
    # log_json = parse_log(jsonfile)
    all_violations = result_dict.get('violations', [])
    violations_count = len(all_violations)
    simplified_violations_list = []
    for element in all_violations:
        simplified_violation = {
            "description": element.get("description"),
            "help": element.get("help"),
            "helpUrl": element.get("helpUrl"),
            "id": element.get("id"),
            "impact": element.get("impact"),
            "tags": element.get("tags", [])
        }
        original_nodes = element.get('nodes', [])
        simplified_nodes = []
        for node in original_nodes:
            simplified_node = {
                "failureSummary": node.get("failureSummary"),
                "html": node.get("html"),
                "target": node.get("target")
            }
            simplified_nodes.append(simplified_node)
        simplified_violation["nodes"] = simplified_nodes
        simplified_violations_list.append(simplified_violation)
    violations_dict = {"violations": simplified_violations_list}
    return violations_count, violations_dict


def flatten_for_dataframe(violations_dict):
    flattened_data = []
    all_violations = violations_dict.get('violations', [])
    for violation in all_violations:
        base_info = {
            "id": violation.get("id"),
            "impact": violation.get("impact"),
            "description": violation.get("description"),
            "help": violation.get("help"),
            "helpUrl": violation.get("helpUrl"),
            "tags": ", ".join(violation.get("tags", []))
        }
        nodes = violation.get('nodes', [])
        if not nodes:
            row = base_info.copy()
            row.update({
                "failureSummary": None,
                "html": None,
                "target": None
            })
            flattened_data.append(row)
        else:
            for node in nodes:
                row = base_info.copy()
                row.update({
                    "failureSummary": node.get("failureSummary"),
                    "html": node.get("html"),
                    "target": ", ".join(node.get("target", []))
                })
                flattened_data.append(row)
    return flattened_data
