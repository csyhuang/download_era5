import codecs
import lxml.html as lh
import pandas as pd

f = codecs.open("/Users/claresyhuang/Downloads/era5.htm", 'r')
html_str = f.read()

doc = lh.fromstring(html_str)
tbody_elements = doc.xpath('//tbody')


def extract_xth_table(i):
    loop_list = list(tbody_elements[i].getiterator(tag='td'))
    if len(loop_list) % 7 == 0:
        num_of_cols = 7
    elif len(loop_list) % 8 == 0:
        num_of_cols = 8
    else:
        raise ValueError("Issues with row count.")

    num_of_rows = len(loop_list) // num_of_cols
    print(f'i: {i}, num_of_rows: {num_of_rows}')
    if num_of_cols == 8:
        pandas_dict = {
            'count': [],
            'name': [],
            'units': [],
            'Variable name in CDS': [],
            'shortName': [],
            'paramId': [],
            'an': [],
            'fc': []
        }
    else:
        pandas_dict = {
            'count': [],
            'name': [],
            'units': [],
            'shortName': [],
            'paramId': [],
            'an': [],
            'fc': []
        }
    begin_index = 1

    for j in range(begin_index, num_of_rows):
        pandas_dict['count'].append(loop_list[num_of_cols * j].text_content())
        pandas_dict['name'].append(loop_list[num_of_cols * j + 1].text_content())
        pandas_dict['units'].append(loop_list[num_of_cols * j + 2].text_content())
        if num_of_cols == 8:
            pandas_dict['Variable name in CDS'].append(loop_list[num_of_cols * j + 3].text_content())
            pandas_dict['shortName'].append(loop_list[num_of_cols * j + 4].text_content())
            pandas_dict['paramId'].append(loop_list[num_of_cols * j + 5].text_content())
            pandas_dict['an'].append(loop_list[num_of_cols * j + 6].text_content())
            pandas_dict['fc'].append(loop_list[num_of_cols * j + 7].text_content())
        else:
            pandas_dict['shortName'].append(loop_list[num_of_cols * j + 3].text_content())
            pandas_dict['paramId'].append(loop_list[num_of_cols * j + 4].text_content())
            pandas_dict['an'].append(loop_list[num_of_cols * j + 5].text_content())
            pandas_dict['fc'].append(loop_list[num_of_cols * j + 6].text_content())
    return pd.DataFrame(pandas_dict)


h3_elements = doc.xpath('//h3')
table_name_list = [elements.text_content().strip() for elements in h3_elements]

m = 0
for k in range(3, 3+len(h3_elements)):
    df = extract_xth_table(k)

    if len(df) < 5:
        continue
    m += 1
    table_name = table_name_list[m]
    save_csv_name = table_name.split(':')[0].replace(' ', '_') + '.csv'

    if table_name == 'Table 14: Satellite Data':
        break

    df.to_csv(save_csv_name, sep='|', index=False)

    print('=================================================')
    print(f'k = {k}. table_name = {table_name}. save_csv_name = {save_csv_name}')
    print(df)
    print('=================================================')
