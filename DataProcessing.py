import pandas as pd
from collections import OrderedDict

class DataProcessing:

    def __init__(self, jotform_client, form_id):
        self.__jotform_client = jotform_client
        self.__form_filter = {'form_id': form_id,'status':'ACTIVE'}

    def get_all_df(self):
        forms = self.__jotform_client.getting_answer(self.__form_filter, limit=1000)

        submissions_df = self.__get_submissions_df(forms)
        crop_counts = self.__crop_cultivated_df(submissions_df)
        irrigation_time = self.__irrigation_time_df(submissions_df)

        return submissions_df, crop_counts, irrigation_time

    def __get_submissions_df(self, submissions):
        forms_normalized = pd.json_normalize(submissions, max_level=0)
        all_submissions = []

        for index, row in forms_normalized.iterrows():

            submission_dict = {}

            submission_dict['id'] = row['id']
            submission_dict['created_at'] = row['created_at']

            form_answers = row['answers']

            form_answers_sorted = OrderedDict(sorted(form_answers.items(), key=lambda x: int(x[1]['order'])))

            # qn: question number, qf:dict of question fields('text','name','order',answer etc.)
            for qn, qf in form_answers_sorted.items():
                question = qf.get('name', 'N/A')
                answer = qf.get('prettyFormat', qf.get('answer', 'N/A'))

                submission_dict[question] = answer

            all_submissions.append(submission_dict)

        df = pd.DataFrame(all_submissions)

        return df


    def __crop_cultivated_df(self, submissions_df):
        crop_data = submissions_df[['District', 'CropCultivated']]
        crop_data = crop_data.assign(CropCultivated=crop_data['CropCultivated'].str.split('; ')).explode(
            'CropCultivated')
        CropList = ['Grape', 'Kapia Peppers', 'Olive', 'Peach', 'Strawberry', 'Tomato', 'Walnut']
        crop_data['CropCultivated'] = crop_data['CropCultivated'].apply(lambda x: x if x in CropList else 'Other')
        crop_counts = crop_data.groupby(['District', 'CropCultivated']).size().reset_index(name='Count')
        return crop_counts

    def __irrigation_time_df(self, submissions_df):
        irrigation_time = submissions_df[['District', 'IrrigationTime']]
        irrigation_time = irrigation_time.assign(IrrigationTime=irrigation_time['IrrigationTime'].str.split('; ')).explode(
            'IrrigationTime')
        irrigation_time = irrigation_time.groupby(['District', 'IrrigationTime']).size().reset_index(name='Count')
        irrigation_time['IrrigationTime'] = irrigation_time['IrrigationTime'].str.split('(', n=1).str[0].str.strip()
        return irrigation_time








