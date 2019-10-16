# load libraries
library(data.table)
library(tidyverse)

# read data
data_flat <- fread('Data/Clean Data/mouse_flat_v2.csv')
mouse_new_var <- fread('Data/Clean Data/mouse_flat_v2.csv')
validation <- fread('Data/validations.csv')
votes <- fread('Data/Clean Data/votes_v2.csv')
user_with_response <- fread('Data/Extra/users_with_absolute_response_features.csv')
mouse_direction <- fread('Data/Clean Data/mouse_user_direction.csv')



#------------------------------------------------------------------------Add Speed 
data_flat <- data_flat[, `Speed`:= distance/time_since]
data_flat[is.na(data_flat$Speed)]$Speed <- 0
data_flat[data_flat$Speed == 'Inf'] <- 0

write.csv(data_flat, 'Data/Clean Data/mouse_flat_v2.csv')

# speed metrics 

speed_metrics <- data_flat[, .(`Max Speed` = max(Speed), 
              `Avg Speed` = mean(Speed), 
              `Sd Speed` = sd(Speed)),
              by = user_id]


#------------------------------------------------------------------------ Action
# group by action and count the number of occurences 
action_count <-
  data_flat[, .(`Action Count` = .N), by = c('user_id', 'action')]

# generate a column for each action type and change the columns names 
action_count_wide <-
  pivot_wider(data = action_count,
              names_from = 'action',
              values_from = 'Action Count')

# delete NP columns 
action_count_wide$np <- NULL

# rename columns 
colnames(action_count_wide) <-c("user_id", "scroll count", "mouse movement count", "click count")

#------------------------------------------------------------------------ Time lapse
# Calculate Total Time to complete survey 
max_time <- data_flat[, .(`Total Time` = max(time_since)), by = user_id]

#------------------------------------------------------------------------ Number of records 
# number of observations per user observation per user
user_record_count <- data_flat[, .(`User Record Count` = .N), by = user_id]

#------------------------------------------------------------------------ Distance
# calculate the total distance traveled by each user 
total_distance <- mouse_new_var[,.(`Total Distance` = sum(distance)), by = user_id]


#------------------------------------------------------------------------ min and max 
# calculate the min and max votes values per user id 
min_score <- votes[,.(`Min Score Value` = min(score)), by = user_id]
max_score <- votes[,.(`Max Score Value` = max(score)), by = user_id]


#------------------------------------------------------------------------ votes

# Aggregate each answers and record number 

new_var <- str_split(votes$value, pattern = '_', simplify = TRUE)
votes$question_type <- new_var[,1]

votes_clean <- votes[,c('user_id','question_type', 'score')]
votes_clean_summarize <- votes_clean[,.(count = .N), by = c('user_id','question_type', 'score')]

votes_clean_summarize$votes_consolidated <- paste(votes_clean_summarize$question_type,'_votes_',
                                                  votes_clean_summarize$score,'_count')

votes_clean_summarize$score <- NULL
votes_clean_summarize$question_type <- NULL

votes_wide <- pivot_wider(data = votes_clean_summarize, names_from = 'votes_consolidated',
                          values_from = 'count')

votes_wide[is.na(votes_wide)] <- 0 

#------------------------------------------------------------------------ Direction 
# select varibles of interest from directions data 

mouse_direction_subset <- 
  mouse_direction %>%
  select(
    user_id,
    measure_width_covered,
    measure_height_covered,
    movesleft,
    movesright,
    no_horizontal_movement,
    perc_left_movement,
    perc_right_movement,
    perc_no_movement_x,
    movesup,
    movesdown,
    no_vertical_movement,
    perc_upwward_movement,
    perc_downward_movement,
    perc_no_movement_y,
  )

#------------------------------------------------------------------------ Add pc name 
# add relevant pc names 
pc.name <- data_flat%>%
  select(user_id,system)
pc.name <- unique(pc.name)

#------------------------------------------------------------------------ combination

merged_data <- merge(x = action_count_wide, y = user_record_count, by = "user_id", all.x = TRUE)
merged_data <- merge(x = merged_data, y = max_time, by = "user_id", all.x = TRUE)
merged_data <- merge(x = merged_data, y = total_distance, by = "user_id", all.x = TRUE)
merged_data <- merge(x = merged_data, y = validation, by = "user_id", all.x = TRUE)
merged_data <- merge(x = merged_data, y = min_score, by = "user_id", all.x = TRUE)
merged_data <- merge(x = merged_data, y = max_score, by = "user_id", all.x = TRUE)
merged_data <- merge(x = merged_data, y = votes_wide, by = "user_id", all.x = TRUE)
merged_data <- merge(x = merged_data, y = mouse_direction_subset, by = "user_id", all.x = TRUE)
merged_data <- merge(x = merged_data, y = pc.name, by = "user_id", all.x = TRUE)
merged_data <- merge(x = merged_data, y = speed_metrics, by = "user_id", all.x = TRUE)

merged_data[is.na(merged_data)] <- 0 

write.csv(merged_data, 'Data/Clean Data/merged_data_user_level.csv')

