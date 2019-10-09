# load libraries
library(data.table)
library(tidyverse)

# read data
data_flat <- fread('Data/mouse-flat.csv')



#------------------------------------------------------------------------ Action

# group by action and count the number of occurences 
action_count <-
  data_flat[, .(`Action Count` = .N), by = c('user_id', 'action')]

# generate a column for each action type and change the columns names 
action_count_wide <-
  pivot_wider(data = action_count,
              names_from = 'action',
              values_from = 'Action Count')

action_count_wide <-
  colnames(action_count_wide) <-
  c("user_id", "scroll count", "mouse movement count", "click count")


#------------------------------------------------------------------------ Time lapse
# max time lapse per user
max_time <- data_flat[, .(`Max Time Lapse` = max(time_since)), by = user_id]


#------------------------------------------------------------------------ Number of records 
# number of observations per user 
user_record_count <- data_flat[, .(`User Record Count` = .N), by = user_id]


#------------------------------------------------------------------------ Distance
Mouse_movement_data <- fread("Data/Mouse_movement.csv")

