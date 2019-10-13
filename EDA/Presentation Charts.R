# set working directory
setwd(
  'C:\\Users\\ander\\Google Drive\\Columbia\\Fall 2019\\Capstone\\Dotin-Columbia-Castone-Team-Alpha-\\Data'
)


# library
library(tidyverse)
library(data.table)
library(ggthemes)

# read csv
mouse.flat <- fread("mouse_new_var.csv")
mouse.flat$radio_adj <- ifelse(mouse.flat$radio == '', 0, 1)

# count radio
count.radio.summary <-
  mouse.flat[, .(`Sum Radio` = sum(radio_adj)), by = user_id]


ggplot(data = count.radio.summary, aes(x = `Sum Radio`)) +
  geom_histogram(fill = '#00ade7') +
  xlab('Radio Clicks') + ylab('Count') + theme_base() + xlim(0, 500) + theme_base()


# time taken by user to complete survey

time.taken.summary <-
  mouse.flat[, .(`Time Elapse` = max(time_since)), by = user_id]

ggplot(data = time.taken.summary, aes(x = `Time Elapse`)) +
  geom_histogram(fill = '#00ade7') +
  xlab('Time Taken') + ylab('Count') + theme_base() + xlim(0, 1500)
