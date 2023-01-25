# FLO_CLTV PREDICT
###########################################
TASK 1: Data Preparation
###########################################
#!pip install lifetimes
import datetime as dt
import pandas as pd
import matplotlib.pyplot as plt
from lifetimes import BetaGeoFitter
from lifetimes import GammaGammaFitter
from lifetimes.plotting import plot_period_transactions

pd.set_option('display.max_columns', None)
pd.set_option('display.width', 500)
from sklearn.preprocessing import MinMaxScaler

#Step 1:
df_ = pd.read_csv("FLO_CLTV_Tahmini/flo_data_20k.csv")

df = df_.copy()
df.describe().T
df.isnull().sum()

#Step 2:


def outlier_thresholds(dataframe, variable):
    quartile1 = dataframe[variable].quantile(0.01)
    quartile3 = dataframe[variable].quantile(0.99)
    interquantile_range = quartile3 - quartile1
    up_limit = quartile3 + 1.5 * interquantile_range
    low_limit = quartile1 - 1.5 * interquantile_range
    return low_limit, up_limit


def replace_with_thresholds(dataframe, variable):
    low_limit, up_limit = outlier_thresholds(dataframe, variable)
    dataframe.loc[(dataframe[variable] < low_limit), variable] = round(low_limit, 0)
    dataframe.loc[(dataframe[variable] > up_limit), variable] = round(up_limit, 0)

#Step 3:

num_cols = ["order_num_total_ever_online", "order_num_total_ever_offline",
            "customer_value_total_ever_offline", "customer_value_total_ever_online"]

for col in num_cols:
    replace_with_thresholds(df, col)

df.describe().T

#Step 4:

df["omni_channel_count"] = df["order_num_total_ever_online"] + df["order_num_total_ever_offline"]
df["omni_channel_sum"] = df["customer_value_total_ever_online"] + df["customer_value_total_ever_offline"]

df.head()

# Step 5:

date_change = df.columns[df.columns.str.contains("date")]
df[date_change] = df[date_change].apply(pd.to_datetime)
df.info()


################################
# Task 2: Creating CLTV Data Structure
################################

# Step 1:

df["last_order_date"].max()
today_date = dt.datetime(2021, 6, 1)
type(today_date)
df.info()

#Step 2:

cltv_df = pd.DataFrame()
cltv_df["customer_id"] = df["master_id"]
cltv_df["recency_cltv_weekly"] = ((df["last_order_date"] - df["first_order_date"]).astype('timedelta64[D]')) / 7
cltv_df["T_weekly"] = ((today_date - df["first_order_date"]).astype('timedelta64[D]')) / 7
cltv_df["Frequency"] = df["omni_channel_count"]
cltv_df["monetary_cltv_avg"] = df["omni_channel_sum"] / df["omni_channel_count"]

cltv_df.head()
cltv_df.describe().T

###########################
# Task 3: Establishment of BG/NBD, Gamma-Gamma Models and Calculation of CLTV
###########################

# Step1: Fit the BG/NBD model.
# • Estimate expected purchases from customers in 3 months and cltv as exp_sales_3_month
# Add it to the dataframe.

bgf = BetaGeoFitter(penalizer_coef=0.001)

bgf.fit(cltv_df["Frequency"],
        cltv_df["recency_cltv_weekly"],
        cltv_df["T_weekly"])

cltv_df["exp_sales_3_month"] = bgf.predict(4 * 3,
                                           cltv_df["Frequency"],
                                           cltv_df["recency_cltv_weekly"],
                                           cltv_df["T_weekly"])

cltv_df.sort_values("exp_sales_3_month", ascending=False)

# Estimate expected purchases from customers in 6 months and cltv as exp_sales_6_month
# add it to the dataframe.

cltv_df["exp_sales_6_month"] = bgf.predict(4 * 6,
                                           cltv_df["Frequency"],
                                           cltv_df["recency_cltv_weekly"],
                                           cltv_df["T_weekly"])

cltv_df.sort_values("exp_sales_6_month", ascending=False)

# Step2: Fit the Gamma-Gamma model. cltv as exp_average_value by estimating the average value that customers will leave
# add to dataframe

ggf = GammaGammaFitter(penalizer_coef=0.01)

ggf.fit(cltv_df["Frequency"], cltv_df["monetary_cltv_avg"])

cltv_df["exp_average_value"] = ggf.conditional_expected_average_profit(cltv_df["Frequency"],
                                                                       cltv_df["monetary_cltv_avg"])

cltv_df.sort_values("exp_average_value", ascending=False)
cltv_df.head()

plot_period_transactions(bgf)
plt.show(block=True)

#Step3: Calculate 6 months CLTV and add it to the dataframe with the name cltv.
# Observe the 20 people with the highest Cltv value.

cltv = ggf.customer_lifetime_value(bgf,
                                   cltv_df["Frequency"],
                                   cltv_df['recency_cltv_weekly'],
                                   cltv_df['T_weekly'],
                                   cltv_df['monetary_cltv_avg'],
                                   time=6,
                                   freq="W",
                                   discount_rate=0.01)

cltv_df["cltv"] = cltv
cltv_df.head()
cltv_df.sort_values("cltv", ascending=False).head(20)

######################################
#Task 4: Creating Segments by CLTV Value
#####################

#Step1: Divide all your customers into 4 groups (segments) according to 6-month CLTV and add the group names to the dataset.

cltv_df["cltv_segment"] = pd.qcut(cltv_df["cltv"], 4, labels=["D", "C", "B", "A"])

cltv_df.head()
