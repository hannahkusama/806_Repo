#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 25 15:13:58 2020

@author: sg
"""

import pandas as pd

def get_tickers(path):
    companies = pd.read_csv(path)
    ticker_list = list(companies['Ticker'])
    print('Retrieved', str(len(ticker_list)), 'ticker symbols.')
    return ticker_list

import quandl
 
def get_prices(ticker):
    print('Retrieving data for', ticker)
    prices = quandl.get('WIKI/' + ticker)['Adj. Close'].reset_index()
    prices['Ticker'] = ticker
    return prices
 
data = []
 
ticker_list = get_tickers('/Users/sg/Documents/GitHub/806_Repo/Labs/module_1/Web_Scraping/your-code/companies.csv')
 
for ticker in ticker_list:
    prices = get_prices(ticker)
    data.append(prices)

def concat_pivot(data, rows, columns, values):
    df = pd.concat(data, sort=True)
    pivot = df.pivot_table(values=values, columns=columns, index=rows)
    return pivot

def compute_returns(df):
    returns = df.pct_change()
    return returns

def return_risk_ratio(df, days=30):
    means = pd.DataFrame(df.tail(days).mean())
    std = pd.DataFrame(df.tail(days).std())
    ratios = pd.concat([means, std], axis=1).reset_index()
    ratios.columns = ['Company', 'Mean', 'Std']
    ratios['Ratio'] = ratios['Mean']/ratios['Std']
    return ratios

#top10 = ratios.sort_values('Ratio', ascending=False).head(10)

def corr_matrix(df, days=30):
    corr_matrix = df.tail(days).corr()
    return corr_matrix
 
#target_list = returns[list(top10['Company'])]
#correlation = corr_matrix(target_list)

import matplotlib.pyplot as plt
import seaborn as sns
 
def barchart(df, x, y, length=8, width=14, title=""):
    df = df.sort_values(x, ascending=False)
    plt.figure(figsize=(width,length))
    chart = sns.barplot(data=df, x=x, y=y)
    plt.title(title + "\n", fontsize=16)
    return chart
 
#bar_plot = barchart(top10, 'Ratio', 'Company', title='Stock Return vs. Risk Ratios')

import numpy as np

def correlation_plot(corr, title=""):
    mask = np.zeros_like(corr, dtype=np.bool)
    mask[np.triu_indices_from(mask)] = True

    plt.subplots(figsize=(15, 10))
    cmap = sns.diverging_palette(6, 255, as_cmap=True)
    
    chart = sns.heatmap(corr, mask=mask, cmap=cmap, center=0, linewidths=.5, annot=True, fmt='.2f')
    plt.title(title, fontsize=16)
    return chart

#corr_plot = correlation_plot(correlation, title='Stock Return Correlation')

def save_viz(chart, title):
    fig = chart.get_figure()
    fig.savefig(title + '.png')
    
pivot=concat_pivot(data, 'Date', 'Ticker', 'Adj. Close')
returns=compute_returns(pivot)

ratios=return_risk_ratio(returns)
top10 = ratios.sort_values('Ratio', ascending=False).head(10)
target_list = returns[list(top10['Company'])]
correlation = corr_matrix(target_list)
bar_plot = barchart(top10, 'Ratio', 'Company', title='Stock Return vs. Risk Ratios')
corr_plot = correlation_plot(correlation, title='Stock Return Correlation')