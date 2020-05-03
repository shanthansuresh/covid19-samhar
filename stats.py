import pandas as pd
import matplotlib.pyplot as plt

class Stats():
  def __init__(self, stats_base_path='out'):
    self.stats_base_path = stats_base_path

    #column_names = ["timestamp", "crowdcount"]
    #self.df = pd.DataFrame(columns=column_names)

    # Timestamp list
    self.ts_list = []
  
    #Crowdcount list
    self.ccount_list = []  

  def update(self, x_val, y_val):
    self.ts_list.append(x_val)
    self.ccount_list.append(y_val)

  def update_plot(self):
    plt.grid()
    plt.xlabel('Timestamp')
    plt.ylabel('CrowdCount')
    plt.plot(self.ts_list, self.ccount_list)
    stats_fig_path = self.stats_base_path + '/' + 'stats.png'
    plt.savefig(stats_fig_path)  

    
    fig = plt.figure()
    plt.grid()
    plt.xlabel('Timestamp')
    plt.ylabel('CrowdCount')
    plt.bar(self.ts_list, self.ccount_list, width=0.25)
    stats_fig_path = self.stats_base_path + '/' + 'stats_bar.png'
    plt.savefig(stats_fig_path)  
    
