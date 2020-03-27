# PEcAn GSoC evaluation task

### Task 1

I tried to build with docker but failed. I found there are no related issues so I guess maybe there is some compatibility problem for building with docker on Windows. I just created an issue on [github page](https://github.com/PecanProject/pecan/issues/2554).

Since you send me the output, I didn't try further to build it in virtual machine. I'll try it later.



### Task 2

For this task, I write the function "getNDVI()" in python file.

The function filtered the images needed for certain place, time range and cloud cover rate. Then it calculates the NDVI map from red and near-infrared bands, and reduce the whole map/matrix to the mean value for comparison.

Some points including:

1. **Use Landsat 7 for comparison** 

   Although Landsat 8 was launched in 2013, I noticed Landsat 7 was launched in 1999 so it covers the time range of LAI output, thus I chose to use Landsat 7 dataset for comparison in the same location and time range, to make it meaningful. Notice the Landsat 8 add Coastal aerosol band so the index of these two datasets would be different. For Landsat 7, red band is B3, near-infrared is B4, and for Landsat 8, it's B4 and B5.

2. **Empirical parameters choosing**

   To use reduceRegion function in GEE, the region should be less than 10^7 pixels, but one single image would have above 5*10^7 pixels. As a result, I triplet the scale, from 30m to 90m, to satisfy the requirement. The same situation is for selecting the threshold of cloud_cover. Due to the thick cloud would significantly change the original NDVI, so I think there would be some empirical values for choosing (also I believe there should be some algorithms to filter them out). Since setting this threshold to 1, as the youtube video shows, would only filter out 11 images, I changed it to 5 with 39 images, for better coverage on this time range.

3.  **Coordinates choosing**

   In web platform, I found the image filtered with our point actually even didn't cover that point. Right now I haven't found information about this problem, and due to slightly change longitude from -105.55 to -105.70  could cover our point, and also cover more of the forest, I would discuss these two situations separately at the end.

   <img src=".\img\coordiante.png" alt="coordinate" style="zoom:50%;" />

4. **Reuse**

   Though the code for this task would not be reused I guess, for better simulating the real task this summer, I still try to make it reusable. So I extract the information of coordinates and time range out of config xml, thus it could be reuse for input in the same format.

   

### Task 3

For this task, I write functions getLVI() and makeplot().

Function getLVI load information from RData format into pandas dataframe in python. Extract time information for later plotting.

Function makeplot make plot with the output of above functions, df_LVI and df_NDVI, which including respective values and corresponding datetimes,  in the same panel for better comparison. In this function, I fixed the range of two y-axis, sacrificing reuse for better looking. 



### Results

From the graph, we could find clear assimilation between LAI from model and NDVI from GEE on annual change. One major difference is LAI shows a higher vegetation index on Autumn 2004 than other years, while NDVI stays the same.

 ![50](.\img\50.png)

The setup of the above graph is 50% threshold for cloud coverage, and the coordinate I slightly change to better cover the point and the forest. 

Actually, we can find assimilation, more or less, on each graph below. But we could also derive some information from comparison of different parameters.

The first one is the higher cloud coverage threshold will not harm the result too much. Although it could have larger local fluctuation, it also better shows the change overall.

Another one is the result of slightly changed coordinate, shows more stable change locally than the original one. I think one intuitive reason could be since plants take larger percentage of the whole area, it should have more stable result on parameters evaluating plants.

![Comparison](.\img\comparison.png)

It's a great task I should say, although I haven't work much on PEcAn, at least I'm in great favor for GEE right now. I think nobody would dislike changing the map - where you actually live in - in the way you want it to be. And also, as a computer science and environmental science student myself, my career goal is to build better software for environmental researchers. I really appreciate the possible chance for me to work with people who have the same goal. I believe I got the basic ideas for what I possibly would do in the summer. I just wondered how should I arrange the timeline? Should I split time for building several links like this or do you have some advice?

I'll send you my draft proposal as soon as possible. And thank you so much for your time.