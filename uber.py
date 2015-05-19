import pandas as pd
from datetime import datetime
import statsmodels.formula.api as sm
import dateutil.parser
 
_get_day_of_wk = lambda x:x.weekday() + 1
_get_hour = lambda x:x.hour + 1
_get_days_since_epoch = lambda x:(x - datetime.utcfromtimestamp(0)).days

class UberPredictor(object):

  def __init__(self, json_path):
    self.reference = json_path

  @property
  def data(self):
      return self.__json_to_df()

  @property
  def regressor(self):
      return self.__create_regressor()

  def __json_to_df(self):
    
    j = pd.read_json(self.reference)
    df = pd.DataFrame(j)
    df['Date'] = pd.to_datetime(df[0])
    df['Count'] = 1
    df = df.set_index('Date').drop(0, axis=1)
    
    resamp = df.resample('H', how=sum)
    resamp.reset_index(drop=False, inplace=True)
    resamp['DoW'] = resamp['Date'].apply(_get_day_of_wk)
    resamp['Hour'] = resamp['Date'].apply(_get_hour)
    resamp['DsE'] = resamp['Date'].apply(_get_days_since_epoch)
    resamp.fillna(0, inplace=True)
    resamp.drop('Date', axis=1, inplace=True)
   
    return resamp

  def __create_regressor(self):

    df = self.data
    f0 = 'Count ~ DsE + C(DoW):C(Hour)'
    results = sm.ols(formula=f0, data=df).fit()

    return results

  def predict_on_date(self, dt_string):
    """Returns a demand prediction based on provided reference."""
    dt = dateutil.parser.parse(dt_string)
    dse = _get_days_since_epoch(dt)
    dow = _get_day_of_wk(dt)
    hour = _get_hour(dt)

    # regressor.predict needs to be fed iterables to make
    # its predictions. For now, we only want it to predict
    # single dates. We can always take out the regressor's
    # own predict method to use on lists.

    if not isinstance(dse, list):
      dse = [dse]

    if not isinstance(dow, list):
      dow = [dow]

    if not isinstance(hour, list):
      hour = [hour]

    return round(self.regressor.predict({'DsE': dse, \
                    'DoW': dow, 'Hour': hour})[0])

if __name__ == '__main__':

  up = UberPredictor('data/uber.json')
  print up.predict_on_date("2012-05-01 18:00:00")
  print up.data
  print up.regressor.summary()