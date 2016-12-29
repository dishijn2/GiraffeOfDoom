import DataPoint as dp
from decimal import Decimal, getcontext
import math
import constants as k
import datafilters as df
import OutputFileManager as ofm

testdata = [
("27/12/2016 9:15",167.9,-2990.08,174.47),
("27/12/2016 9:16",171.55,-2990.08,173.01),
("27/12/2016 9:16",170.09,-2990.08,175.93),
("27/12/2016 9:16",173.01,-2990.08,171.55),
("27/12/2016 9:16",170.09,-2990.08,177.39),
("27/12/2016 9:17",170.09,-2990.08,175.2),
("27/12/2016 9:17",170.82,-2990.08,175.93),
("27/12/2016 9:17",169.36,-2990.08,173.74),
("27/12/2016 9:17",170.82,-2990.08,176.66),
("27/12/2016 9:18",167.17,-2990.08,173.74),
("27/12/2016 9:18",168.63,-2990.08,178.12),
("27/12/2016 9:18",169.36,-2990.08,175.93),
("27/12/2016 9:18",168.63,-2990.08,174.47),
("27/12/2016 9:19",169.36,-2990.08,175.2),
("27/12/2016 9:19",166.44,-2990.08,178.12),
("27/12/2016 9:19",169.36,-2990.08,175.93),
("27/12/2016 9:19",170.82,-2990.08,175.2),
("27/12/2016 9:20",168.63,-2990.08,174.47),
("27/12/2016 9:20",170.09,-2990.08,173.01),
("27/12/2016 9:20",169.36,-2990.08,178.12),
("27/12/2016 9:20",170.09,-2990.08,176.66),
("27/12/2016 9:21",167.9,-2990.08,173.74),
("27/12/2016 9:21",169.36,-2990.08,173.74),
("27/12/2016 9:21",168.63,-2990.08,173.74),
("27/12/2016 9:21",170.82,-2990.08,175.2),
("27/12/2016 9:22",167.9,-2990.08,175.93),
("27/12/2016 9:22",167.9,-2990.08,175.2),
("27/12/2016 9:22",169.36,-2990.08,175.2),
("27/12/2016 9:22",168.63,-2990.08,175.93),
("27/12/2016 9:23",167.9,-2990.08,177.39),
("27/12/2016 9:23",169.36,-2990.08,175.93),
("27/12/2016 9:23",168.63,-2990.08,175.93),
("27/12/2016 9:23",170.09,-2990.08,174.47),
("27/12/2016 9:24",171.55,-2990.08,175.93),
("27/12/2016 9:24",170.82,-2990.08,174.47),
("27/12/2016 9:24",166.44,-2990.08,175.2),
("27/12/2016 9:24",167.9,-2990.08,173.74),
("27/12/2016 9:25",169.36,-2990.08,174.47),
("27/12/2016 9:25",170.09,-2990.08,175.93),
("27/12/2016 9:25",168.63,-2990.08,173.01),
("27/12/2016 9:25",169.36,-2990.08,174.47),
("27/12/2016 9:26",170.82,-2990.08,176.66),
("27/12/2016 9:26",173.01,-2990.08,174.47),
("27/12/2016 9:26",167.17,-2990.08,173.01),
("27/12/2016 9:26",167.17,-2990.08,175.93),
("27/12/2016 9:27",169.36,-2990.08,175.2),
("27/12/2016 9:27",169.36,-2990.08,176.66),
("27/12/2016 9:27",170.82,-2990.08,175.2),
("27/12/2016 9:27",170.09,-2990.08,176.66),
("27/12/2016 9:28",167.17,-2990.08,176.66),
("27/12/2016 9:28",168.63,-2990.08,177.39),
("27/12/2016 9:28",171.55,-2990.08,173.74),
("27/12/2016 9:28",169.36,-2990.08,175.2),
("27/12/2016 9:29",170.09,-2990.08,177.39),
("27/12/2016 9:29",169.36,-2990.08,175.2),
("27/12/2016 9:29",170.09,-2990.08,175.93),
("27/12/2016 9:29",171.55,-2990.08,175.2),
("27/12/2016 9:30",167.9,-2990.08,175.2),
("27/12/2016 9:30",167.9,-2990.08,175.2),
("27/12/2016 9:30",169.36,-2990.08,177.39),
("27/12/2016 9:30",168.63,-2990.08,173.74),
("27/12/2016 9:31",170.82,-2990.08,175.93),
("27/12/2016 9:31",168.63,-2990.08,176.66),
("27/12/2016 9:31",173.01,-2990.08,174.47),
("27/12/2016 9:31",168.63,-2990.08,175.93),
("27/12/2016 9:32",170.09,-2990.08,174.47),
("27/12/2016 9:32",170.09,-2990.08,174.47),
("27/12/2016 9:32",167.17,-2990.08,175.2),
("27/12/2016 9:32",170.82,-2990.08,177.39),
("27/12/2016 9:33",170.09,-2990.08,175.2),
("27/12/2016 9:33",168.63,-2990.08,176.66),
("27/12/2016 9:33",168.63,-2990.08,176.66),
("27/12/2016 9:33",171.55,-2990.08,176.66),
("27/12/2016 9:34",169.36,-2990.08,175.2),
("27/12/2016 9:34",170.82,-2990.08,173.74),
("27/12/2016 9:34",169.36,-2990.08,174.47),
("27/12/2016 9:34",170.82,-2990.08,174.47),
("27/12/2016 9:35",170.82,-2990.08,177.39),
("27/12/2016 9:35",170.09,-2990.08,176.66),
("27/12/2016 9:35",170.09,-2990.08,176.66),
("27/12/2016 9:35",168.63,-2990.08,176.66),
("27/12/2016 9:36",171.55,-2990.08,175.2),
("27/12/2016 9:36",171.55,-2990.08,175.2),
("27/12/2016 9:36",173.01,-2990.08,173.74),
("27/12/2016 9:36",170.09,-2990.08,176.66),
("27/12/2016 9:37",172.28,-2990.08,174.47),
("27/12/2016 9:37",172.28,-2990.08,175.2),
("27/12/2016 9:37",168.63,-2990.08,175.93),
("27/12/2016 9:37",169.36,-2990.08,176.66),
("27/12/2016 9:38",169.36,-2990.08,175.93),
("27/12/2016 9:38",170.09,-2990.08,175.2),
("27/12/2016 9:38",172.28,-2990.08,174.47),
("27/12/2016 9:38",172.28,-2990.08,174.47),
("27/12/2016 9:39",171.55,-2990.08,175.2),
("27/12/2016 9:39",173.74,-2990.08,175.2),
("27/12/2016 9:39",171.55,-2990.08,174.47),
("27/12/2016 9:39",172.28,-2990.08,176.66),
("27/12/2016 9:40",172.28,-2990.08,175.93),
("27/12/2016 9:40",172.28,-2990.08,173.74),
("27/12/2016 9:40",173.74,-2990.08,175.93),
("27/12/2016 9:40",170.09,-2990.08,176.66),
("27/12/2016 9:41",173.01,-2990.08,173.74),
("27/12/2016 9:41",173.74,-2990.08,173.74),
("27/12/2016 9:41",174.47,-2990.08,174.47),
("27/12/2016 9:41",170.82,-2990.08,175.93),
("27/12/2016 9:42",173.74,-2990.08,175.93),
("27/12/2016 9:42",171.55,-2990.08,175.2),
("27/12/2016 9:42",172.28,-2990.08,174.47),
("27/12/2016 9:42",173.01,-2990.08,175.93),
("27/12/2016 9:43",170.82,-2990.08,176.66),
("27/12/2016 9:43",173.74,-2990.08,174.47),
("27/12/2016 9:43",173.01,-2990.08,175.2),
("27/12/2016 9:43",171.55,-2990.08,175.93),
("27/12/2016 9:44",170.09,-2990.08,173.74),
("27/12/2016 9:44",170.82,-2990.08,176.66),
("27/12/2016 9:44",172.28,-2990.08,173.01),
("27/12/2016 9:44",170.82,-2990.08,174.47),
("27/12/2016 9:45",170.82,-2990.08,173.01),
("27/12/2016 9:45",170.82,-2990.08,175.93),
("27/12/2016 9:45",172.28,-2990.08,176.66),
("27/12/2016 9:45",171.55,-2990.08,174.47),
("27/12/2016 9:46",170.82,-2990.08,174.47),
("27/12/2016 9:46",175.2,-2990.08,174.47),
("27/12/2016 9:46",173.74,-2990.08,177.39),
("27/12/2016 9:46",175.93,-2990.08,173.74),
("27/12/2016 9:47",173.01,-2990.08,173.01),
("27/12/2016 9:47",171.55,-2990.08,175.2),
("27/12/2016 9:47",169.36,-2990.08,176.66),
("27/12/2016 9:47",175.2,-2990.08,173.01),
("27/12/2016 9:48",171.55,-2990.08,175.2),
("27/12/2016 9:48",173.74,-2990.08,175.2),
("27/12/2016 9:48",174.47,-2990.08,175.93),
("27/12/2016 9:48",168.63,-2990.08,175.93),
("27/12/2016 9:49",173.01,-2990.08,174.47),
("27/12/2016 9:49",173.01,-2990.08,175.2),
("27/12/2016 9:49",173.01,-2990.08,175.93),
("27/12/2016 9:49",182.5,-2990.08,170.82),
("27/12/2016 9:50",171.55,-2990.08,175.93),
("27/12/2016 9:50",176.66,-2990.08,174.47),
("27/12/2016 9:50",173.74,-2990.08,178.12),
("27/12/2016 9:50",171.55,-2990.08,175.93),
("27/12/2016 9:51",175.93,-2990.08,175.2),
("27/12/2016 9:51",175.2,-2990.08,176.66),
("27/12/2016 9:51",173.01,-2990.08,175.93),
("27/12/2016 9:51",173.74,-2990.08,172.28),
("27/12/2016 9:52",175.2,-2990.08,174.47),
("27/12/2016 9:52",176.66,-2990.08,173.74),
("27/12/2016 9:52",175.93,-2990.08,176.66),
("27/12/2016 9:52",174.47,-2990.08,175.2),
("27/12/2016 9:53",174.47,-2990.08,177.39),
("27/12/2016 9:53",175.2,-2990.08,176.66),
("27/12/2016 9:53",176.66,-2990.08,176.66),
("27/12/2016 9:53",173.74,-2990.08,175.93),
("27/12/2016 9:54",173.01,-2990.08,175.93),
("27/12/2016 9:54",173.01,-2990.08,173.74),
("27/12/2016 9:54",176.66,-2990.08,174.47),
("27/12/2016 9:54",174.47,-2990.08,173.01),
("27/12/2016 9:55",173.74,-2990.08,176.66),
("27/12/2016 9:55",174.47,-2990.08,175.93),
("27/12/2016 9:55",173.74,-2990.08,176.66),
("27/12/2016 9:55",173.01,-2990.08,175.2),
("27/12/2016 9:56",173.74,-2990.08,173.01),
("27/12/2016 9:56",177.39,-2990.08,173.74),
("27/12/2016 9:56",174.47,-2990.08,175.93),
("27/12/2016 9:56",176.66,-2990.08,176.66),
("27/12/2016 9:57",174.47,-2990.08,175.93),
("27/12/2016 9:57",177.39,-2990.08,175.93),
("27/12/2016 9:57",175.93,-2990.08,172.28),
("27/12/2016 9:57",178.85,-2990.08,173.74),
("27/12/2016 9:58",175.93,-2990.08,175.93),
("27/12/2016 9:58",177.39,-2990.08,175.2),
("27/12/2016 9:58",181.04,-2990.08,174.47),
("27/12/2016 9:58",175.2,-2990.08,175.2),
("27/12/2016 9:59",173.74,-2990.08,173.74),
("27/12/2016 9:59",174.47,-2990.08,176.66),
("27/12/2016 9:59",178.85,-2990.08,175.93),
("27/12/2016 9:59",174.47,-2990.08,175.2),
("27/12/2016 10:00",178.12,-2990.08,174.47),
("27/12/2016 10:00",174.47,-2990.08,175.2),
("27/12/2016 10:00",174.47,-2990.08,175.93),
("27/12/2016 10:00",176.66,-2990.08,173.74),
("27/12/2016 10:01",178.85,-2990.08,173.74),
("27/12/2016 10:01",177.39,-2990.08,173.01),
("27/12/2016 10:01",175.93,-2990.08,173.74),
("27/12/2016 10:01",176.66,-2990.08,176.66),
("27/12/2016 10:02",176.66,-2990.08,178.12),
("27/12/2016 10:02",174.47,-2990.08,171.55),
("27/12/2016 10:02",175.2,-2990.08,174.47),
("27/12/2016 10:02",175.93,-2990.08,173.01),
("27/12/2016 10:03",177.39,-2990.08,174.47),
("27/12/2016 10:03",175.2,-2990.08,176.66),
("27/12/2016 10:03",175.2,-2990.08,173.74),
("27/12/2016 10:03",175.2,-2990.08,175.2),
("27/12/2016 10:04",175.93,-2990.08,175.2),
("27/12/2016 10:04",175.93,-2990.08,173.74),
("27/12/2016 10:04",176.66,-2990.08,174.47),
("27/12/2016 10:04",176.66,-2990.08,174.47),
("27/12/2016 10:05",178.12,-2990.08,174.47),
("27/12/2016 10:05",178.12,-2990.08,173.74),
("27/12/2016 10:05",176.66,-2990.08,175.93),
("27/12/2016 10:05",178.12,-2990.08,178.12),
("27/12/2016 10:06",175.93,-2990.08,176.66),
("27/12/2016 10:06",177.39,-2990.08,173.01),
("27/12/2016 10:06",180.31,-2990.08,174.47),
("27/12/2016 10:06",175.93,-2990.08,173.01),
("27/12/2016 10:07",178.85,-2990.08,175.93),
("27/12/2016 10:07",177.39,-2990.08,175.93),
("27/12/2016 10:07",177.39,-2990.08,175.93),
("27/12/2016 10:07",179.58,-2990.08,177.39),
("27/12/2016 10:08",178.85,-2990.08,174.47),
("27/12/2016 10:08",180.31,-2990.08,176.66),
("27/12/2016 10:08",177.39,-2990.08,175.93),
("27/12/2016 10:08",178.12,-2990.08,175.93),
("27/12/2016 10:09",179.58,-2990.08,175.2),
("27/12/2016 10:09",173.74,-2990.08,175.93),
("27/12/2016 10:09",8228.56,235.06,-16630.87),
("27/12/2016 10:09",177.39,-2990.08,174.47),
("27/12/2016 10:10",176.66,-2990.08,173.74),
("27/12/2016 10:10",176.66,-2990.08,175.93),
("27/12/2016 10:10",175.93,-2990.08,175.2),
("27/12/2016 10:10",179.58,-2990.08,172.28),
("27/12/2016 10:11",178.12,-2990.08,174.47),
("27/12/2016 10:11",175.93,-2990.08,174.47),
("27/12/2016 10:11",176.66,-2990.08,174.47),
("27/12/2016 10:11",178.12,-2990.08,175.2),
("27/12/2016 10:12",181.04,-2990.08,175.2),
("27/12/2016 10:12",176.66,-2990.08,175.93),
("27/12/2016 10:12",176.66,-2990.08,173.01),
("27/12/2016 10:12",178.85,-2990.08,174.47),
("27/12/2016 10:13",175.93,-2990.08,174.47),
("27/12/2016 10:13",177.39,-2990.08,175.2),
("27/12/2016 10:13",178.12,-2990.08,175.2),
("27/12/2016 10:13",178.12,-2990.08,175.2),
("27/12/2016 10:14",178.12,-2990.08,175.2),
("27/12/2016 10:14",177.39,-2990.08,175.2),
("27/12/2016 10:14",177.39,-2990.08,177.39),
("27/12/2016 10:14",179.58,-2990.08,173.74),
("27/12/2016 10:15",178.85,-2990.08,175.2),
("27/12/2016 10:15",178.85,-2990.08,175.2),
("27/12/2016 10:15",179.58,-2990.08,177.39),
("27/12/2016 10:15",176.66,-2990.08,175.93),
("27/12/2016 10:16",188.34,-2990.08,172.28),
("27/12/2016 10:16",177.39,-2990.08,174.47),
("27/12/2016 10:16",175.93,-2990.08,175.93),
("27/12/2016 10:16",183.96,-2990.08,173.01),
("27/12/2016 10:17",177.39,-2990.08,173.01),
("27/12/2016 10:17",175.93,-2990.08,175.2),
("27/12/2016 10:17",175.2,-2990.08,173.74),
("27/12/2016 10:17",177.39,-2990.08,175.2),
("27/12/2016 10:18",177.39,-2990.08,175.93),
("27/12/2016 10:18",177.39,-2990.08,176.66),
("27/12/2016 10:18",176.66,-2990.08,174.47),
("27/12/2016 10:18",178.12,-2990.08,173.01),
("27/12/2016 10:19",176.66,-2990.08,174.47),
("27/12/2016 10:19",173.74,-2990.08,173.01),
("27/12/2016 10:19",176.66,-2990.08,175.93),
("27/12/2016 10:19",175.93,-2990.08,174.47),
("27/12/2016 10:20",178.85,-2990.08,175.93),
("27/12/2016 10:20",175.93,-2990.08,176.66),
("27/12/2016 10:20",176.66,-2990.08,174.47),
("27/12/2016 10:20",175.2,-2990.08,175.2),
("27/12/2016 10:21",175.2,-2990.08,175.2),
("27/12/2016 10:21",173.74,-2990.08,175.2),
("27/12/2016 10:21",177.39,-2990.08,175.93),
("27/12/2016 10:21",174.47,-2990.08,175.2),
("27/12/2016 10:22",177.39,-2990.08,174.47),
("27/12/2016 10:22",175.93,-2990.08,176.66),
("27/12/2016 10:22",177.39,-2990.08,174.47),
("27/12/2016 10:22",178.12,-2990.08,173.74),
("27/12/2016 10:23",178.12,-2990.08,177.39),
("27/12/2016 10:23",179.58,-2990.08,176.66),
("27/12/2016 10:23",175.93,-2990.08,174.47),
("27/12/2016 10:23",175.93,-2990.08,177.39),
("27/12/2016 10:24",179.58,-2990.08,175.93),
("27/12/2016 10:24",178.12,-2990.08,175.2),
("27/12/2016 10:24",177.39,-2990.08,173.74),
("27/12/2016 10:24",177.39,-2990.08,174.47),
("27/12/2016 10:25",177.39,-2990.08,175.93),
("27/12/2016 10:25",176.66,-2990.08,175.2),
("27/12/2016 10:25",177.39,-2990.08,175.2),
("27/12/2016 10:25",176.66,-2990.08,174.47),
("27/12/2016 10:26",178.12,-2990.08,176.66),
("27/12/2016 10:26",176.66,-2990.08,172.28),
("27/12/2016 10:26",180.31,-2990.08,172.28),
("27/12/2016 10:26",176.66,-2990.08,174.47),
("27/12/2016 10:27",175.93,-2990.08,176.66),
("27/12/2016 10:27",175.93,-2990.08,173.74),
("27/12/2016 10:27",176.66,-2990.08,174.47),
("27/12/2016 10:27",174.47,-2990.08,173.01),
("27/12/2016 10:28",178.12,-2990.08,174.47),
("27/12/2016 10:28",176.66,-2990.08,173.01),
("27/12/2016 10:28",179.58,-2990.08,172.28),
("27/12/2016 10:28",176.66,-2990.08,175.2),
("27/12/2016 10:29",177.39,-2990.08,171.55),
("27/12/2016 10:29",178.12,-2990.08,178.12),
("27/12/2016 10:29",176.66,-2990.08,178.12),
("27/12/2016 10:29",178.85,-2990.08,176.66),
("27/12/2016 10:30",179.58,-2990.08,173.74),
("27/12/2016 10:30",178.12,-2990.08,176.66),
("27/12/2016 10:30",178.12,-2990.08,173.74)
]

# #################################################################################
# Calculate the differences
# This function will create an array of differences
# #################################################################################
def create_diffs_array(readings_array):
    diffsarray = []
    if len(readings_array) > 2:
        for i in range (1, len(readings_array)):
            # here we deal with flipping. differences should be in the order of 10s. It we're seeing 100s, there's an issue.
            # DIRECTLY set up the difference values for the main reading array datapoints. This is stored to the raw logfiles
            # APPLY field correction - increasing readings should be increasing field strength
            diff_x = (Decimal(readings_array[i].raw_x) - Decimal(readings_array[i-1].raw_x))
            if math.sqrt(math.pow(diff_x,2)) > k.MAG3110_FLIP:
                diff_x = 0

            diff_y = (Decimal(readings_array[i].raw_y) - Decimal(readings_array[i-1].raw_y))
            if math.sqrt(math.pow(diff_y,2)) > k.MAG3110_FLIP:
                diff_y = 0

            diff_z = (Decimal(readings_array[i].raw_z) - Decimal(readings_array[i-1].raw_z))
            if math.sqrt(math.pow(diff_z,2)) > k.MAG3110_FLIP:
                diff_z = 0

            dapt = dp.DataPoint(readings_array[i].dateTime,diff_x, diff_y, diff_z)
            diffsarray.append(dapt)
    else:
        dapt = dp.DataPoint("0000-00-00 00:00:00",0,0,0)
        diffsarray.append(dapt)

    return diffsarray

#################################################
# create the test magdata datapoint array
magdata = []
for item in testdata:
    readings = dp.DataPoint(item[0], item[1], item[2], item[3])
    magdata.append(readings)


output_diffs = create_diffs_array(magdata)


smoothed_data_array = ofm.readings_from_diffs(output_diffs)
ofm.Create24(smoothed_data_array)
ofm.Create4(smoothed_data_array)
ofm.CreateDiffs(output_diffs)  # use output_diffs data