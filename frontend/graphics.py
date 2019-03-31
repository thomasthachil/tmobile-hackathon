from math import pi
import pandas as pd

from bokeh.io import output_notebook, show
from bokeh.palettes import Category20c, viridis
from bokeh.plotting import figure
from bokeh.transform import cumsum
from bokeh.palettes import Spectral6
from bokeh.models import ColumnDataSource

import difflib
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from datetime import datetime

class ChefJeff:
    def __init__(self, db, business):
        self.db = db
        self.id = business
        self.sid = SentimentIntensityAnalyzer()

    def getPopularPhones(self):
        pop_phones = []
        phones = {
            'samsung': [
                's9',
                's8',
                's7',
                'note',
                's6',
            ],
            'apple': ['iphone', 'ipad', 'ipod'],
            'motorola': ['motoX'],
            'google': ['Nexus'],
            'LG': ['g9', 'g5', 'g6', 'g3', 'g4'],
        }
        frequencies = {}

        business_id = self.id
        data = self.db.df.loc[business_id]
        for category in ['key_phrases_pos', 'key_phrases_neg']:
            for dictionary in data[category]:
                for word in dictionary['keyPhrases']:
                    for brand,v in phones.items():
                        for phone in v:
                            seq = difflib.SequenceMatcher(None,word.lower(),phone)
                            d = seq.ratio()*100
                            if(d > 0.75):
                                largest = None
                                smallest = None
                                if(len(phone) > len(word)):
                                    largest = phone
                                    smallest = word
                                else:
                                    largest = word
                                    smallest = phone

                                if(smallest.lower() in largest.lower()):
                                    if(brand in frequencies.keys()):
                                        frequencies[phone] += 1
                                    else:
                                        frequencies[phone] = 1
        return frequencies

    def getServiceSentiment(self):
        sentiment = {'pos': [0, []], 'neg': [0, []], 'neutral': [0, []]}

        business_id = self.id
        data = self.db.df.loc[business_id]
        for category in ['key_phrases_pos', 'key_phrases_neg']:
            for dictionary in data[category]:
                phones = ['customer', 'service']
                for phone in phones:
                    for word in dictionary['keyPhrases']:
                        seq = difflib.SequenceMatcher(None,word.lower(),phone)
                        d = seq.ratio()*100
                        if(d > 0.75):
                            largest = None
                            smallest = None
                            if(len(phone) > len(word)):
                                largest = phone
                                smallest = word
                            else:
                                largest = word
                                smallest = phone

                            if(smallest.lower() in largest.lower()):
                                polarity = self.sid.polarity_scores(largest)['compound']
                                if(polarity == 0.0):
                                    sentiment['neutral'][0] += 1
                                    sentiment['neutral'][1].append(largest)
                                elif(polarity < 0.0):
                                    sentiment['neg'][0] += 1
                                    sentiment['neg'][1].append(largest)
                                else:
                                    sentiment['pos'][0] += 1
                                    sentiment['pos'][1].append(largest)

        return sentiment

    def getPhoneChart(self):
        x = self.getPopularPhones()

        data = pd.Series(x).reset_index(name='value').rename(columns={'index':'models'})
        data['angle'] = data['value']/data['value'].sum() * 2*pi
        data['color'] = viridis(len(x))

        p = figure(plot_height=350, title="Phone useage in Store %s" % (self.id), toolbar_location=None,
                   tools="hover", tooltips="@models: @value", x_range=(-0.5, 1.0))

        p.wedge(x=0, y=1, radius=0.4,
                start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),
                line_color="white", fill_color='color', legend='models', source=data)

        p.axis.axis_label=None
        p.axis.visible=False
        p.grid.grid_line_color = None

        return p

    def getServiceSentimentChart(self):
        x = self.getServiceSentiment()

        source = ColumnDataSource(data=dict(sentiment= list(x.keys()), counts= [v[0] for k,v in x.items()],
                                            color=Spectral6, services = [';'.join(v[1]) for k,v in x.items()]))

        p = figure(x_range = list(x.keys()), title="Service Sentiment for %s" % (self.id),
                   toolbar_location=None, tools="hover", tooltips="@sentiment: @services", plot_width = 800)

        p.vbar(x='sentiment', top='counts', width=0.9, color='color', source=source)

        p.xgrid.grid_line_color = None

        return p

    def getReviewsOverTime(self):

        data = self.db.df.loc[self.id]['time']

        source = ColumnDataSource(data=dict(time = [i[1] for i in data], rating = [i[0] for i in data]))

        p = figure(x_axis_type='datetime',
                   x_axis_label = 'time',
                   y_axis_label = 'ratings',
                   title = "Ratings of %s Over Time" % (self.id),
                   plot_width = 1100
                   )

        p.circle(x='time', y='rating', color='blue', source=source)

        p.xgrid.grid_line_color = None

        return p

    def returnData(self):
        return self.key_phrases

    def getStoreIds(self):
        return list(map(lambda x: x['id'], self.returnData()['documents']))