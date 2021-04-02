# data-viz-python-sdk A toolkit for the auto generation of best practice charts



 data-viz-python-sdk is a toolkit that reads raw data and generates both the best chart to display your data. The output chart is designed to include the best practice of Data Visualisation (Gestalt theory and Pre-attentive attributes)

The initial toolkit provides four possible chart outputs: Bar Chart, Histogram, Line Chart and Scatter plot. We hope that teams find this toolkit useful and build upon the initial quartet of charts.

## Installing the toolkit

### Builds

TBD: link travis build status here!

Automatic builds are executed in travis and new release version created after every PR merge to master branch.

### How to trigger runs on the kubernetes cluster

After every merge to master a new version tag is created, eg [0.2.0] <ADD LINK> - to get that version executed, create a new corresponding `-run` tag eg [0.2.0-run]<ADD LINK>.

Link to create a new release tag: <ADD LINK>

This will trigger a build in travis to retag the existing X.Y.Z version as X.Y.Z-run which will be picked up for execution. You should see a new commit to update the version tag in the deployment manifest eg: <ADD LINK>

Logs can be found in logdna:
1. Login to <PLACEHOLDER>
2. Switch to <PLACEHOLDER> account
3. Go to <PLACEHOLDER>
4. Open <PLACEHOLDER> logdna instance
5. Go to Sugarcane Yield view: <ADD LINK>


## Running the toolkit




## A description of the output


## Next steps from here:

* Update the requirements file with the python dependencies you need.
* Add your sources code into src/analytics-base folder
* Update src/analytics-base/run.sh folder with the code to use your model

