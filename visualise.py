import os
import xml.etree.ElementTree as ET
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def parse_xml_file(xml_path):
    tree = ET.parse(xml_path)
    root = tree.getroot()

    data = []
    metadata = {}

    for child in root:
        if child.tag == 'metadata':
            for meta in child:
                metadata[meta.tag] = meta.text
        elif child.tag == 'entry':
            entry_data = {elem.tag: elem.text for elem in child}
            entry_data.update(metadata)
            data.append(entry_data)

    return data


def load_xml_files(directory):
    all_data = []
    for filename in os.listdir(directory):
        if filename.endswith('.xml'):
            file_path = os.path.join(directory, filename)
            file_data = parse_xml_file(file_path)
            all_data.extend(file_data)

    return pd.DataFrame(all_data)


def save_and_show_plot(fig, filename):
    output_dir = 'plots'
    os.makedirs(output_dir, exist_ok=True)
    fig.savefig(os.path.join(output_dir, filename))
    plt.show()


def visualize_data(df):
    sns.set(font_scale=1.2)

    # Convert numeric columns to appropriate data types
    df['amount_of_turns'] = pd.to_numeric(df['amount_of_turns'])
    df['distinct_clarification_type_count'] = pd.to_numeric(df['distinct_clarification_type_count'])
    df['amount_of_interactions'] = pd.to_numeric(df['amount_of_interactions'])
    df['start_ms'] = pd.to_numeric(df['start_ms'], errors='coerce')

    # Plot distribution of turns
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.histplot(df['amount_of_turns'], kde=True, ax=ax)
    ax.set_title('Distribution of Amount of Turns')
    ax.set_xlabel('Amount of Turns')
    ax.set_ylabel('Frequency')
    save_and_show_plot(fig, 'distribution_of_amount_of_turns.png')

    # Plot distribution of distinct clarification types
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.histplot(df['distinct_clarification_type_count'], kde=True, ax=ax)
    ax.set_title('Distribution of Distinct Clarification Type Count')
    ax.set_xlabel('Distinct Clarification Type Count')
    ax.set_ylabel('Frequency')
    save_and_show_plot(fig, 'distribution_of_distinct_clarification_type_count.png')

    # Plot distribution of interactions
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.histplot(df['amount_of_interactions'], kde=True, ax=ax)
    ax.set_title('Distribution of Amount of Interactions')
    ax.set_xlabel('Amount of Interactions')
    ax.set_ylabel('Frequency')
    save_and_show_plot(fig, 'distribution_of_amount_of_interactions.png')

    # Count plot of clarification types
    fig, ax = plt.subplots(figsize=(14, 8))
    sns.countplot(y='clarification_type', data=df, order=df['clarification_type'].value_counts().index, ax=ax)
    ax.set_title('Frequency of Clarification Types')
    ax.set_xlabel('Count')
    ax.set_ylabel('Clarification Type')
    save_and_show_plot(fig, 'frequency_of_clarification_types.png')

    # Box plot of amount of turns by gender
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.boxplot(x='gender', y='amount_of_turns', data=df, ax=ax)
    ax.set_title('Amount of Turns by Gender')
    ax.set_xlabel('Gender')
    ax.set_ylabel('Amount of Turns')
    save_and_show_plot(fig, 'amount_of_turns_by_gender.png')


def main():
    input_dir = 'xml_annotations'
    df = load_xml_files(input_dir)
    visualize_data(df)


if __name__ == '__main__':
    main()
