import json
import glob
import os

json_dir = 'output_json_files/'

output_sql_file = 'insert_statements.sql'

initial_rule_id = 52

insert_template = """INSERT INTO `amasty_shiprestriction_rule` (`rule_id`, `is_active`, `for_admin`, `out_of_stock`, `all_stores`, `all_groups`, `name`, `coupon`, `discount_id`, `days`, `time_from`, `time_to`, `stores`, `cust_groups`, `message`, `carriers`, `methods`, `conditions_serialized`, `coupon_disable`, `discount_id_disable`) VALUES ({rule_id}, 1, 1, 0, 0, 0, 'Exceptions', NULL, '', '7,1,2,3,4,5,6', 1, 2346, '1,2,3', '0,1,4,5,6', NULL, 'flatrate,jadlog,,,', NULL, '{conditions_serialized}', NULL, '');"""

def generate_insert_statement(json_file, rule_id):
    with open(json_file, 'r') as f:
        data = json.load(f)
    
    conditions_serialized = json.dumps(data, separators=(',', ':')).replace("\\", "\\\\").replace("'", "''")
    
    return insert_template.format(rule_id=rule_id, conditions_serialized=conditions_serialized)

json_files = glob.glob(os.path.join(json_dir, "*.json"))

with open(output_sql_file, 'w') as f:
    for idx, json_file in enumerate(json_files):
        # Increment rule_id for each JSON file
        rule_id = initial_rule_id + idx
        # Generate and write the insert statement for each JSON file
        insert_statement = generate_insert_statement(json_file, rule_id)
        f.write(insert_statement + '\n')

print(f"SQL insert statements have been written to {output_sql_file}")
