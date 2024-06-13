import csv
import xml.etree.ElementTree as ET
import os
from xml.dom import minidom

DTD = '''<!DOCTYPE dialogue [
<!ELEMENT dialogue (metadata, entry*)>
<!ELEMENT metadata (gender, age_group, nationality, first_language, english_skills, education, tech_savviness, date_of_interaction, amount_of_turns, distinct_clarification_type_count, amount_of_interactions)>
<!ELEMENT gender (#PCDATA)>
<!ELEMENT age_group (#PCDATA)>
<!ELEMENT nationality (#PCDATA)>
<!ELEMENT first_language (#PCDATA)>
<!ELEMENT english_skills (#PCDATA)>
<!ELEMENT education (#PCDATA)>
<!ELEMENT tech_savviness (#PCDATA)>
<!ELEMENT date_of_interaction (#PCDATA)>
<!ELEMENT amount_of_turns (#PCDATA)>
<!ELEMENT distinct_clarification_type_count (#PCDATA)>
<!ELEMENT amount_of_interactions (#PCDATA)>
<!ELEMENT entry (start_ms, speaker, text, clarification_turn, clarification_type, clarification_span?)>
<!ELEMENT start_ms (#PCDATA)>
<!ELEMENT speaker (#PCDATA)>
<!ELEMENT text (#PCDATA)>
<!ELEMENT clarification_turn (#PCDATA)>
<!ELEMENT clarification_type (#PCDATA)>
<!ELEMENT clarification_span (#PCDATA)>
]>'''


def create_xml_element(parent, tag, text):
    element = ET.SubElement(parent, tag)
    element.text = text or ''
    return element


def load_metadata(metadata_path):
    metadata_dict = {}
    with open(metadata_path, 'r', newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            participant_id = row['participant id']
            metadata_dict[participant_id] = {
                'gender': row['gender'],
                'age_group': row['age group'],
                'nationality': row['nationality'],
                'first_language': row['first language'],
                'english_skills': row['english skills'],
                'education': row['education'],
                'tech_savviness': row['tech-savviness'],
                'date_of_interaction': row['date of interaction'],
                'amount_of_turns': row['amount of turns']
            }
    return metadata_dict


def add_metadata_to_xml(parent, metadata, distinct_clarification_type_count, interaction_count):
    metadata_elem = ET.SubElement(parent, 'metadata')
    for key, value in metadata.items():
        create_xml_element(metadata_elem, key, value)
    create_xml_element(metadata_elem, 'distinct_clarification_type_count', str(distinct_clarification_type_count))
    create_xml_element(metadata_elem, 'amount_of_interactions', str(interaction_count))


def find_clarification_span(text, clarification_text):
    try:
        start_index = text.index(clarification_text)
        end_index = start_index + len(clarification_text)
        return [start_index, end_index]
    except ValueError:
        return None


def process_csv_row(row):
    entry = ET.Element('entry')
    create_xml_element(entry, 'start_ms', row.get('start (in ms)'))
    create_xml_element(entry, 'speaker', row.get('speaker'))
    text = row.get('text').lower()
    create_xml_element(entry, 'text', text)
    create_xml_element(entry, 'clarification_turn', row.get('turn agreement'))
    create_xml_element(entry, 'clarification_type', row.get('type agreement'))

    clarification_text = row.get('clarification text', '').strip().lower()
    if clarification_text:
        clarification_span = find_clarification_span(text, clarification_text)
        if clarification_span:
            create_xml_element(entry, 'clarification_span', str(clarification_span))

    return entry


def count_distinct_clarification_types_and_interactions(csv_path):
    clarification_types = set()
    interaction_count = 0
    interaction_phrases = [
        '((temi turns around))',
        '((temi goes to the kitchen))',
        '((temi comes to participant))'
    ]

    with open(csv_path, 'r', newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            clarification_type = row.get('type agreement')
            if clarification_type:
                clarification_types.add(clarification_type)
            if row.get('text'):
                text = row['text']
                for phrase in interaction_phrases:
                    if phrase in text:
                        interaction_count += 1
                        break

    return len(clarification_types), interaction_count


def convert_csv_to_xml(csv_path, metadata_dict):
    root = ET.Element('dialogue')

    # Extract participant ID from the CSV filename
    participant_id = os.path.basename(csv_path).split('.')[0]
    if participant_id in metadata_dict:
        distinct_clarification_type_count, interaction_count = count_distinct_clarification_types_and_interactions(
            csv_path)
        add_metadata_to_xml(root, metadata_dict[participant_id], distinct_clarification_type_count, interaction_count)

    with open(csv_path, 'r', newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            entry = process_csv_row(row)
            root.append(entry)

    xml_data = ET.tostring(root, encoding='unicode')
    xml_with_dtd = DTD + '\n' + xml_data
    pretty_xml = minidom.parseString(xml_with_dtd).toprettyxml(indent="    ")

    return pretty_xml


def write_xml_file(xml_data, output_path):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(xml_data)


def main():
    input_dir = 'csv_annotations'
    output_dir = 'xml_annotations'
    metadata_path = 'metadata.csv'

    metadata_dict = load_metadata(metadata_path)
    csv_files = os.listdir(input_dir)

    for csv_file in csv_files:
        csv_path = os.path.join(input_dir, csv_file)
        xml_data = convert_csv_to_xml(csv_path, metadata_dict)
        xml_file = os.path.join(output_dir, f'participant_{csv_file.replace(".csv", ".xml")}')
        write_xml_file(xml_data, xml_file)
        print(f'XML file "{xml_file}" created successfully.')


if __name__ == '__main__':
    main()
