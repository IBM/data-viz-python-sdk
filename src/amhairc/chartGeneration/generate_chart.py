from bokeh.embed import file_html
from bokeh.layouts import row, column
from bokeh.models import BoxZoomTool, ColumnDataSource, DatetimeTickFormatter, Div, HoverTool, PanTool, ResetTool, SaveTool
from bokeh.plotting import figure
from bokeh.resources import CDN
from bokeh.transform import factor_cmap

import src.amhairc.chartSelection.chart_identification as ci


import numpy as np
import pandas as pd

class Chart:

    def __init__(
            self,
            chartD,
            chart_found,
            dataframe,
            plot_width,
            plot_height,
            about,
            chart_location):
        self.chartD = chartD
        self.chart_found = chart_found
        self.dataframe = dataframe
        self.plot_width = plot_width
        self.plot_height = plot_height
        self.about = about
        self.chart_location = chart_location
        self.chart = self.generate_chart()

        print("At the very start: CHARTD", chartD)

    # TO DO: Import ChartType(Enum) from identify_charts.py
    def generate_chart(self):

        if str(self.chart_found) == "lineplot":
            chart = LinePlot(
                self.chartD,
                self.chart_found,
                self.dataframe,
                self.plot_width,
                self.plot_height,
                self.about).build_chart()
            html = file_html(chart, CDN, "AMHAIRC Line plot")

        elif str(self.chart_found) == "groupedscatter":
            chart = ScatterPlot(
                self.chartD,
                self.chart_found,
                self.dataframe,
                self.plot_width,
                self.plot_height,
                self.about).build_chart()
            html = file_html(
                chart, CDN, "AMHAIRC Scatter plot")

        elif str(self.chart_found) == ci.ChartType.HISTOGRAM:
            chart = Histogram(
                self.chartD,
                self.chart_found,
                self.dataframe,
                self.plot_width,
                self.plot_height,
                self.about).build_chart()
            html = file_html(chart, CDN, "AMHAIRC Histogram")

        elif str(self.chart_found) == "barplot":
            chart = BarPlot(
                self.chartD,
                self.chart_found,
                self.dataframe,
                self.plot_width,
                self.plot_height,
                self.about).build_chart()
            html = file_html(chart, CDN, "AMHAIRC Bar plot")

        elif str(self.chart_found) == "boxplot":
            chart = BoxPlot(
                self.chartD,
                self.chart_found,
                self.dataframe,
                self.plot_width,
                self.plot_height,
                self.about).build_chart()
            html = file_html(chart, CDN, "AMHAIRC Box plot")

        print("self.chart_found", self.chart_found)

        text_file = open(
            self.chart_location,
            "w")

        if html:
            text_file.write(html)
        else:
            text_file.write("No Chart Generated")

        text_file.close()

        return self.chart_location


class SuperPlot:

    def __init__(
            self,
            chartD,
            chart_found,
            dataframe,
            plot_width,
            plot_height,
            about):
        self.plot_width = plot_width
        self.plot_height = plot_height
        self.chart_found = chart_found
        self.dataframe = dataframe
        self.chartD = chartD
        self.about = about


    def apply_styles(self, plot, chart_found):
        # Outlines
        plot.outline_line_alpha = 0

        # Title
        plot.title.align = "center"
        plot.title.text_color = "#343334"
        plot.title.text_font = "IBM Plex Sans"
        plot.title.text_font_size = "12pt"

        # Figure
        plot.border_fill_alpha = 0
        plot.background_fill_alpha = 1
        plot.background_fill_color = "#ffffff"

        # Axis lines
        plot.xaxis.axis_line_alpha = 0.25
        plot.yaxis.axis_line_alpha = 0.25
        plot.xaxis.axis_line_width = 2
        plot.yaxis.axis_line_width = 2

        # Axis labels
        plot.xaxis.axis_label_text_font = "IBM Plex Sans"
        plot.yaxis.axis_label_text_font = "IBM Plex Sans"

        # Grid lines
        if self.chart_found == 'scatterplot' or self.chart_found == 'groupedscatter':
            plot.xgrid.grid_line_color = "#aeb3b7"
            plot.xgrid.grid_line_dash = "dotted"
            plot.xgrid.grid_line_alpha = 0.5

            plot.ygrid.grid_line_color = "#aeb3b7"
            plot.ygrid.grid_line_dash = "dotted"
            plot.xgrid.grid_line_alpha = 0.5
        else:
            plot.xgrid.grid_line_color = None
            plot.ygrid.grid_line_color = None

        # Tickers
        plot.xaxis.major_tick_line_alpha = 0
        plot.yaxis.major_tick_line_alpha = 0

        plot.xaxis.minor_tick_line_alpha = 0
        plot.yaxis.minor_tick_line_alpha = 0

        # Bokeh logo
        plot.toolbar.logo = None

        # Legend only where needed
        if chart_found == "histogram":
            pass
        elif chart_found == "boxplot":
            pass
        else:
            plot.legend.label_text_font = "IBM Plex Sans"

        return plot

    def add_tools(self, plot, source, datetime_bool):
        """ tip_labels is a list of values which match the keys of the plot's source dictionary """
        plot.tools = [PanTool(), BoxZoomTool(), SaveTool(), ResetTool()]

        key_names = list(source.data.keys())

        if 'chart_colors' in key_names:
            key_names.remove('chart_colors')

        names = key_names
        tips = []

        if datetime_bool:
            tips.append((names[0], '@' + names[0] + '{%F}'))
            tips.append((names[1], '@' + names[1]))

            hovertool = HoverTool(
                tooltips=tips,
                formatters={
                    '@' + names[0]: 'datetime'},
                mode='vline'
            )

        else:
            for tip in names:
                tips.append((tip, '@' + tip))

            hovertool = HoverTool(
                tooltips=tips,
                mode='vline'
            )

        plot.add_tools(hovertool)
        return plot

    def make_title_text(
            self,
            chart_found,
            dataframe,
            chartD,
            x_column_name_from_index):
        """ TODO: Does not yet work for scatter and bar plots.
            Finalization of title_text to follow from consultation with Jonathan. """
        if chart_found == "timeseries":
            title_text = ["Trend of"]
        elif chart_found == "scatterplot" or chart_found == "groupedscatter" or chart_found == "lineplot":
            title_text = "Relationship between " + \
                ", ".join(dataframe.columns.tolist())
        elif chart_found == "histogram":
            title_text = [
                "Histogram of " +
                chartD +
                " data"][0]
        elif chart_found == "barplot":
            title_text = ["Count of " + x_column_name_from_index][0]
        elif chart_found == "boxplot":
            title_holder = []
            for column_name in dataframe.columns:
                title_holder.append(str(column_name))
                title_holder.append(" vs ")
            title_text = ''.join(title_holder[:-1])
        else:
            title_text = ["Other title..."][0]

        return title_text


class BoxPlot(SuperPlot):
    """
        This LinePlot extends SuperPlot (inheriting all parent's properties and methods)
    """

    def __init__(
            self,
            chartD,
            chart_found,
            dataframe,
            plot_width,
            plot_height,
            about):
        super().__init__(chartD, chart_found, dataframe, plot_width, plot_height, about)
        self.number_of_series = chartD['chartCriteria']['series'].values.tolist()[
            0]
        self.column_names = dataframe.columns.tolist()
        self.x_column_name_from_index = self.column_names[chartD['X']]
        self.y_column_names = [
            i for i in self.column_names + [
                self.x_column_name_from_index] if i not in self.column_names or i not in [
                self.x_column_name_from_index]]

    def build_chart(self):
        title_text = self.make_title_text(
            self.chart_found,
            self.dataframe,
            self.chartD,
            self.x_column_name_from_index)

        type_of_data = self.chartD['chartCriteria']['datacat'].values

        if type_of_data == ['numcat']:
            cats = self.dataframe[self.x_column_name_from_index].unique().tolist()
        else:
            cats = self.dataframe.columns.tolist()

        p = figure(
            plot_width=self.plot_width,
            plot_height=self.plot_height,
            title=title_text,
            tools=['pan', 'box_zoom', 'save', 'reset'],
            x_range=cats,
        )

        charting_resources = self.make_source(cats, self.dataframe, type_of_data)

        mins = charting_resources[0]
        maxes = charting_resources[1]
        q1_list = charting_resources[2]
        q2_list = charting_resources[3]
        q3_list = charting_resources[4]

        # Draw the primary 'boxes'
        p.vbar(cats, 0.7, q2_list, q3_list, fill_color="#436584", line_color="black")
        p.vbar(cats, 0.7, q1_list, q2_list, fill_color="#da9539", line_color="black")

        # stems
        p.segment(cats, maxes, cats, q3_list, line_color="black")
        p.segment(cats, mins, cats, q1_list, line_color="black")

        # whiskers (almost-0 height rects simpler than segments)
        p.rect(cats, mins, 0.2, 0.01, line_color="black")
        p.rect(cats, maxes, 0.2, 0.01, line_color="black")
        p.rect(cats, q2_list, 0.7, 0.01, line_color="black")

        p.y_range.start = 0
        styled_plot = self.apply_styles(p, self.chart_found)
        styled_plot.left[0].formatter.use_scientific = False

        div = Div(text=self.about, width=900)
        chart_obj = column(row(styled_plot), row(div))
        return chart_obj

    def make_source(self, categorical_items, df, type_of_data):

        mins = []
        maxes = []
        q1_list = []
        q2_list = []
        q3_list = []

        def make_quartiles(list_sorted):
            q1_list.append(np.quantile(list_sorted, q=0.25))
            q2_list.append(np.quantile(list_sorted, q=0.5))
            q3_list.append(np.quantile(list_sorted, q=0.75))

            return q1_list, q2_list, q3_list

        if type_of_data == ['numcat']:
            factor_1 = self.x_column_name_from_index
            factor_2 = self.y_column_names[0]

            categorical_items = df[factor_1].unique().tolist()

            data = pd.DataFrame({factor_1: df[factor_1], factor_2: df[factor_2]})

            data[factor_1] = data[factor_1].astype(str)

            for categorical_value in categorical_items:
                target_column = data.loc[(data[factor_1] == categorical_value)]

                mins.append(target_column[factor_2].min())
                maxes.append(target_column[factor_2].max())

                list_sorted = sorted(target_column[factor_2].tolist())
                q1_list, q2_list, q3_list = make_quartiles(list_sorted)

        else:
            for categorical_value in categorical_items:
                target_column = df[categorical_value].tolist()

                mins.append(min(target_column))
                maxes.append(max(target_column))

                list_sorted = sorted(target_column)
                q1_list, q2_list, q3_list = make_quartiles(list_sorted)

        return mins, maxes, q1_list, q2_list, q3_list


class LinePlot(SuperPlot):
    """
        This LinePlot extends SuperPlot (inheriting all parent's properties and methods)
    """

    def __init__(
            self,
            chartD,
            chart_found,
            dataframe,
            plot_width,
            plot_height,
            about):
        super().__init__(chartD, chart_found, dataframe, plot_width, plot_height, about)
        self.datetime_flag = chartD['chartCriteria']['datacat'].tolist()[
            0] == "timeseries"
        self.number_of_series = chartD['chartCriteria']['series'].values.tolist()[
            0]
        self.column_names = dataframe.columns.tolist()
        self.x_column_name_from_index = self.column_names[chartD['X']]
        self.y_column_names = [
            i for i in self.column_names + [
                self.x_column_name_from_index] if i not in self.column_names or i not in [
                self.x_column_name_from_index]]

    def build_chart(self):
        title_text = self.make_title_text(
            self.chart_found,
            self.dataframe,
            self.chartD,
            self.x_column_name_from_index)
        x_axis_label_text = self.x_column_name_from_index
        # TODO: Waiting on Jonathan's opinion regarding user input labels
        y_axis_label_text = ""

        if self.datetime_flag:
            p = figure(
                plot_width=self.plot_width,
                plot_height=self.plot_height,
                title=title_text,
                x_axis_type="datetime",
                x_axis_label=x_axis_label_text,
                y_axis_label=y_axis_label_text)
        else:
            p = figure(
                plot_width=self.plot_width,
                plot_height=self.plot_height,
                title=title_text,
                x_axis_label=x_axis_label_text,
                y_axis_label=y_axis_label_text)

        source = self.make_source(self.chartD, self.dataframe)
        colors = ['#003e6b', '#cf922c', '#6f0000', 'pink', 'green']

        if self.number_of_series == '1':
            p.line(
                x=self.x_column_name_from_index,
                y=self.y_column_names[0],
                legend_label=self.y_column_names[0],
                line_color=colors[0],
                source=source)
        else:
            for i in range(0, len(self.y_column_names)):
                p.line(x=self.x_column_name_from_index,
                       y=self.y_column_names[i],
                       legend_label=self.y_column_names[i],
                       line_color=colors[:len(self.y_column_names)][i],
                       source=source)

        p.add_layout(p.legend[0], 'right')
        p.legend[0].border_line_color = None
        p.xaxis.formatter = DatetimeTickFormatter(months=["%Y-%m-%d"])

        p = self.add_tools(p, source, self.datetime_flag)

        styled_plot = self.apply_styles(p, self.chart_found)

        div = Div(text=self.about, width=900)
        chart_obj = column(row(styled_plot), row(div))
        return chart_obj

    def make_source(self, chartD, df):
        if self.datetime_flag:
            print("In make source:" + str(df[self.x_column_name_from_index]))
            df[self.x_column_name_from_index] = pd.to_datetime(
                df[self.x_column_name_from_index], utc=True)

        if self.number_of_series == '1':
            print(
                "self.y_column_names",
                self.y_column_names[0],
                type(
                    self.y_column_names))
            # if there are multi-series
            data = {self.x_column_name_from_index: df[self.x_column_name_from_index].tolist(
            ), self.y_column_names[0]: df[self.y_column_names[0]].tolist()}

        else:
            data = {
                self.x_column_name_from_index: df[self.x_column_name_from_index].tolist()}

            for i in range(0, len(self.y_column_names)):
                data[self.y_column_names[i]] = df[self.y_column_names[i]].tolist()

        source = ColumnDataSource(data=data)

        return source


class ScatterPlot(SuperPlot):
    """
        This ScatterPlot extends SuperPlot (inheriting all parent's properties and methods)
        - datetime_bool: Boolean (True or False depending on if the x_range data is datetime or not)
    """

    def __init__(
            self,
            chartD,
            chart_found,
            dataframe,
            plot_width,
            plot_height,
            about):
        super().__init__(chartD, chart_found, dataframe, plot_width, plot_height, about)
        self.number_of_series = chartD['chartCriteria']['series'].values.tolist()[
            0]
        self.column_names = dataframe.columns.tolist()
        self.x_column_name_from_index = self.column_names[chartD['X']]
        self.y_column_names = [
            i for i in self.column_names + [
                self.x_column_name_from_index] if i not in self.column_names or i not in [
                self.x_column_name_from_index]]  # Gotten by subtracting column 'X' from all columns in dataframe

    def build_chart(self):
        title_text = self.make_title_text(
            self.chart_found,
            self.dataframe,
            self.chartD,
            self.x_column_name_from_index)
        x_axis_label_text = self.y_column_names[0]
        y_axis_label_text = self.y_column_names[1]

        x_max = self.dataframe[self.y_column_names[0]].max()
        x_min = self.dataframe[self.y_column_names[0]].min()
        y_min = 0
        y_max = self.dataframe[self.y_column_names[1]].max()

        p = figure(
            plot_width=self.plot_width,
            plot_height=self.plot_height,
            title=title_text,
            x_axis_label=x_axis_label_text,
            y_axis_label=y_axis_label_text,
            x_range=(x_min, x_max*1.2),
            y_range=(y_min, y_max+(y_max/20)) # Just gives a little buffer)
        )

        if self.chart_found == "groupedscatter":
            source = self.make_source(
                self.chartD, self.chart_found, self.dataframe)

            p.circle(
                x=self.y_column_names[0],
                y=self.y_column_names[1],
                fill_color='chart_colors',
                line_color=None,
                alpha=1,
                legend_field=self.x_column_name_from_index,
                size=10,
                source=source)

        p.add_layout(p.legend[0], 'right')
        p.legend[0].border_line_color = None
        p = self.add_tools(p, source, None)
        styled_plot = self.apply_styles(p, self.chart_found)
        div = Div(text=self.about, width=900)
        chart_obj = column(row(styled_plot), row(div))
        return chart_obj

    def make_source(self, chartD, chart_found, dataframe):

        # 1. Figure out what kind of scatter it is
        if chart_found == "groupedscatter":
            # if there are multi-series
            categories = dataframe[self.x_column_name_from_index].unique(
            ).tolist()

            # Make the colormap
            colors = ['#436584', '#da9539', '#8c4e1a', '#afb3b7', '#7f7f7f']
            colormap = {}
            for i in range(0, len(categories)):
                colormap[categories[i]] = colors[i]

            colors = [colormap[x]
                      for x in dataframe[self.x_column_name_from_index].tolist()]

            # Add the categorical data
            data = {
                self.x_column_name_from_index: dataframe[self.x_column_name_from_index].tolist()}

            # Add the numerical data
            for i in range(0, len(self.y_column_names)):
                data[self.y_column_names[i]] = dataframe[self.y_column_names[i]].tolist()

            # Add the colors
            data['chart_colors'] = colors

        source = ColumnDataSource(data=data)

        return source


class Histogram(SuperPlot):
    """
    A histogram takes numeric input only. The variable is cut into several bins, and the number of observation per bin is represented by the height of the bar.

    This Histogram extends SuperPlot (inheriting all parent's properties and methods)
    """

    def __init__(
            self,
            chartD,
            chart_found,
            dataframe,
            plot_width,
            plot_height,
            about):
        super().__init__(chartD, chart_found, dataframe, plot_width, plot_height, about)
        self.number_of_series = chartD['chartCriteria']['series'].values.tolist()[
            0]
        self.column_names = dataframe.columns.tolist()
        self.x_column_name_from_index = self.column_names[chartD['X']]
        self.y_column_names = [
            i for i in self.column_names + [
                self.x_column_name_from_index] if i not in self.column_names or i not in [
                self.x_column_name_from_index]]  # Gotten by subtracting column 'X' from all columns in dataframe

    def build_chart(self):
        plot_holder = []

        for i in range(0, int(self.number_of_series)):

            hist, edges = np.histogram(
                self.dataframe[self.column_names[i]].tolist(), density=True, bins=50)
            title_text = self.make_title_text(
                self.chart_found,
                self.dataframe,
                self.column_names[i],
                self.x_column_name_from_index)

            # set the boundaries for the chart.
            x_max = self.dataframe[self.column_names[i]].max()
            x_min = self.dataframe[self.column_names[i]].min()
            y_min = 0
            y_max = hist.max()  # Largest value from the density function

            p = figure(plot_width=self.plot_width,
                       plot_height=self.plot_height,
                       title=title_text,
                       x_axis_label=self.column_names[i],
                       # The Y axis is essentially the probability density function of x i.e. P(x)
                       y_axis_label=str("P(" + self.column_names[i] + ")"),
                       x_range=(x_min, x_max * 1.2),
                       # Just gives a little buffer
                       y_range=(y_min, y_max + (y_max / 20))
                       )

            # Construct the histogram
            p.quad(top=hist,
                   bottom=0,
                   left=edges[:-1],
                   right=edges[1:],
                   fill_color="#4a6581",
                   line_color="white",
                   alpha=0.7)

            hover = HoverTool(tooltips = [('Value', '@top{1.1111}')], mode='vline')
            p.add_tools(hover)

            styled_plot = self.apply_styles(p, self.chart_found)
            styled_plot.left[0].formatter.use_scientific = False
            plot_holder.append(styled_plot)

        div = Div(text=self.about, width=900)
        chart_obj = column(row(plot_holder), row(div))
        return chart_obj


class BarPlot(SuperPlot):
    """
        This Bar plot class extends SuperPlot (inheriting all parent's properties and methods)
    """

    def __init__(
            self,
            chartD,
            chart_found,
            dataframe,
            plot_width,
            plot_height,
            about):
        super().__init__(chartD, chart_found, dataframe, plot_width, plot_height, about)
        self.number_of_series = chartD['chartCriteria']['series'].values.tolist()[
            0]
        self.column_names = dataframe.columns.tolist()
        self.x_column_name_from_index = self.column_names[chartD['X']]
        self.y_column_names = [
            i for i in self.column_names + [
                self.x_column_name_from_index] if i not in self.column_names or i not in [
                self.x_column_name_from_index]]

    def build_chart(self):
        df = self.dataframe
        title_text = self.make_title_text(
            self.chart_found,
            self.dataframe,
            self.chartD,
            self.x_column_name_from_index)
        x_axis_label_text = self.x_column_name_from_index
        # Question: Will the y_label of a barchart always be "counts"?
        y_axis_label_text = "Counts"

        categorical_items = self.dataframe[self.x_column_name_from_index].unique(
        ).tolist()
        p = figure(
            x_range=categorical_items,
            plot_width=self.plot_width,
            plot_height=self.plot_height,
            title=title_text,
            x_axis_label=x_axis_label_text,
            y_axis_label=y_axis_label_text)

        count_per_item = []
        for item in categorical_items:
            count = len(
                df[df[self.x_column_name_from_index].str.strip() == item])
            count_per_item.append(count)

        source = ColumnDataSource(
            data={str(self.x_column_name_from_index): categorical_items, 'counts':count_per_item}
            )

        max_five_colors = [
            "#4a6581",
            "#d0974b",
            "#855026",
            "#b0b3b7",
            "#7f7f7f"]

        p.vbar(
            x=self.x_column_name_from_index,
            top='counts',
            width=0.9,
            source=source,
            legend_field=self.x_column_name_from_index,
            line_color='white',
            fill_color=factor_cmap(
                self.x_column_name_from_index,
                palette=max_five_colors,
                factors=categorical_items))

        p.add_layout(p.legend[0], 'right')
        p.legend[0].border_line_color = None
        p.y_range.start = 0

        p = self.add_tools(p, source, None)
        styled_plot = self.apply_styles(p, self.chart_found)
        div = Div(text=self.about, width=900)
        chart_obj = column(row(styled_plot), row(div))
        return chart_obj

    def make_source(self, df, categorical_items):

        count_per_item = []
        for item in categorical_items:
            count = len(
                df[df[self.x_column_name_from_index].str.strip() == item])
            count_per_item.append(count)

        data = {self.x_column_name_from_index: categorical_items,
                'counts': count_per_item}

        source = ColumnDataSource(data=data)

        return source
