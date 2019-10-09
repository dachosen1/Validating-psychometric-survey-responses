# load libraries
library(data.table)
library(tidyverse)

# read data
data_flat <- fread('Data/mouse-flat.csv')
mouse_new_var <- fread('Data/mouse_new_var.csv')
validation <- fread('Data/validations.csv')

#------------------------------------------------------------------------ Action

# group by action and count the number of occurences 
action_count <-
  data_flat[, .(`Action Count` = .N), by = c('user_id', 'action')]

# generate a column for each action type and change the columns names 
action_count_wide <-
  pivot_wider(data = action_count,
              names_from = 'action',
              values_from = 'Action Count')

colnames(action_count_wide) <-c("user_id", "scroll count", "mouse movement count", "click count")

#------------------------------------------------------------------------ Time lapse
# max time lapse per user
max_time <- data_flat[, .(`Max Time Lapse` = max(time_since)), by = user_id]


#------------------------------------------------------------------------ Number of records 
# number of observations per user 
user_record_count <- data_flat[, .(`User Record Count` = .N), by = user_id]

#------------------------------------------------------------------------ Distance
# total distance traveled by each  user 
total_distance <- mouse_new_var[,.(`Total Distance` = .N), by = user_id]


#------------------------------------------------------------------------ combination

merged_data <- merge(x = action_count_wide, y = user_record_count, by = "user_id", all.x = TRUE)
merged_data <- merge(x = merged_data, y = max_time, by = "user_id", all.x = TRUE)
merged_data <- merge(x = merged_data, y = total_distance, by = "user_id", all.x = TRUE)
merged_data <- merge(x = merged_data, y = validation, by = "user_id", all.x = TRUE)

write.csv(merged_data, 'Data/Clean Data/Clean_data.csv')


