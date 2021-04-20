class HeatMap {
    /*
    The code below will change
    the heading with id = "myH"
    and the paragraph with id = "myP"
    in my web page:
    */

    constructor(data, scale) {
        /*
        The code below will change
        the heading with id = "myH"
        and the paragraph with id = "myP"
        in my web page:
        */

        // Extracts the samples and the code paths
        this.data = data;
        this.scale = scale;
        this.Samples = d3.map(this.data, function (d) { return d.sample_id; }).keys()
        this.CodePaths = d3.map(this.data, function (d) { return d.path; }).keys()

        // Setting the dimensions, margins and the color palette of the graph
        this.margin = { top: 110, right: 10, bottom: 100, left: 50 };
        this.width = 1920 - this.margin.left - this.margin.right;
        this.height = 1400 - this.margin.top - this.margin.bottom;
        this.ColorPalette = ['#f1bc31', '#e9731e', '#e4671f', '#df5a21', '#bc2d23']

    }

    create_tooltip() {
        /*
        The code below will change
        the heading with id = "myH"
        and the paragraph with id = "myP"
        in my web page:
        */
        var tooltip = d3.select("#heatmap")
            .append("div")
            .style("position", "absolute")
            .style("opacity", 0)
            .attr("class", "tooltip")
            .style("background-color", "white")
            .style("border", "solid")
            .style("border-width", "2px")
            .style("border-radius", "5px")
            .style("padding", "5px")
            .style("direction", "ltr")
            .style("background-color", "white")
            .style("border", "solid")
            .style("border-width", "1px")
            .style("border-radius", "5px")
            .style("padding", "10px")

        return tooltip
    }

    create_mouse_over_event(tooltip) {
        /*
        The code below will change
        the heading with id = "myH"
        and the paragraph with id = "myP"
        in my web page:
        */
        return function (d) {
            tooltip
                .style("opacity", 1)

            d3.select(this)
                .style("stroke", "black")
                .style("opacity", 1)
        }
    }

    create_mouse_move_event(tooltip) {
        /*
        The code below will change
        the heading with id = "myH"
        and the paragraph with id = "myP"
        in my web page:
        */
        return function (d) {

            var mouse_position = Math.abs(event.clientX);
            if (mouse_position > 550) {
                var tooltip_position = d3.event.pageX - 10 - tooltip.node().getBoundingClientRect().width + "px"
            } else {
                var tooltip_position = d3.event.pageX + 10 + "px"
            }

            tooltip
                .html(d.tooltip)
                .style("left", tooltip_position)
                .style("top", d3.event.pageY + 10 + "px")
        }
    }

    create_mouse_leave_event(tooltip) {
        /*
        The code below will change
        the heading with id = "myH"
        and the paragraph with id = "myP"
        in my web page:
        */
        return function (d) {
            tooltip
                .style("opacity", 0)
            d3.select(this)
                .style("stroke", "none")
                .style("opacity", 0.8)
        }

    }

    create_mouse_click_event(meta_data) {
        /*
        The code below will change
        the heading with id = "myH"
        and the paragraph with id = "myP"
        in my web page:
        */
        var meta_data_viewer = document.getElementById("meta_data_viewer")

        // Generate human friendly code path
        var code_path = "";
        for (const method of meta_data.hierarchy) {
            method = method.replace(/[^\w\s]/gi, '')
            if (code_path == "") {

                var code_path = method;

            } else {

                var code_path = code_path + " --> " + method;
            }
        }
        console.log(code_path)
        meta_data_viewer.innerHTML = code_path;
    }

    create_color_palette() {
        /*
        The code below will change
        the heading with id = "myH"
        and the paragraph with id = "myP"
        in my web page:
        */
        return d3.scaleLinear()
            .range(this.ColorPalette)
            .domain(this.scale)
    }

    create_x_axis(svg) {
        /*
        The code below will change
        the heading with id = "myH"
        and the paragraph with id = "myP"
        in my web page:
        */
        // Build X axis:
        var x_axis = d3.scaleBand()
            .range([0, this.width])
            .domain(this.Samples)
            .padding(0.05)

        // text label for the x axis
        svg.append("text")
            .attr("x", 925)
            .attr("y", 1225)
            .style("font-size", 30)
            .style("text-anchor", "middle")
            .text("Samples");

        return x_axis
    }

    create_y_axis(svg) {
        /*
        The code below will change
        the heading with id = "myH"
        and the paragraph with id = "myP"
        in my web page:
        */
        var y_axis = d3.scaleBand()
            .range([this.height, 0])
            .domain(this.CodePaths)
            .padding(0.05);

        // text label for the y axis
        svg.append("text")
            .attr("x", 600)
            .attr("y", 30)
            .attr("transform", "rotate(90)")
            .style("font-size", 30)
            .style("text-anchor", "middle")
            .text("Code Paths");

        return y_axis

    }

    create_title_and_subtitle(svg) {
        /*
        The code below will change
        the heading with id = "myH"
        and the paragraph with id = "myP"
        in my web page:
        */
        // Add title to graph
        svg.append("text")
            .attr("x", 10)
            .attr("y", -50)
            .attr("text-anchor", "left")
            .style("font-size", 50)
            .text("QuickPotato Code Path Heatmap");

        // Add subtitle to graph
        svg.append("text")
            .attr("x", 10)
            .attr("y", -10)
            .attr("text-anchor", "left")
            .style("font-size", 25)
            .style("fill", "grey")
            .style("max-width", 400)
            .text("A short description of the take-away message of this chart.");
    }

    render() {
        /*
        The code below will change
        the heading with id = "myH"
        and the paragraph with id = "myP"
        in my web page:
        */

        // Add the svg image to the page and generate the color palette
        var svg = d3.select("#heatmap")
            .append("svg")
            .attr("viewBox", `0 0 1920 1400`)
            .append("g")
            .attr("transform", "translate(" + this.margin.left + "," + this.margin.top + ")");
        var Color = this.create_color_palette();

        // Create the mouse and tooltip event handlers
        var tooltip = this.create_tooltip();
        var mouseover = this.create_mouse_over_event(tooltip);
        var mousemove = this.create_mouse_move_event(tooltip);
        var mouseleave = this.create_mouse_leave_event(tooltip);
        var mouseclick = this.create_mouse_click_event;

        // Build the X axis:
        var x_axis = this.create_x_axis(svg);

        // Build the Y axis:
        var y_axis = this.create_y_axis(svg);

        // Add all the code paths per sample as squares
        svg.selectAll()
            .data(this.data, function (d) { return d.sample_id + ':' + d.path; })
            .enter()
            .append("rect")
            .attr("x", function (d) { return x_axis(d.sample_id) })
            .attr("y", function (d) {
                console.log(d.path)
                return y_axis(d.path)
            })
            .attr("rx", 4)
            .attr("ry", 4)
            .attr("width", x_axis.bandwidth())
            .attr("height", y_axis.bandwidth())
            .style("fill", function (d) { return Color(d.time) })
            .style("stroke-width", 4)
            .style("stroke", "none")
            .style("opacity", 0.8)
            .on("mouseover", mouseover)
            .on("mousemove", mousemove)
            .on("mouseleave", mouseleave)
            .on("click", mouseclick);

        // Create title and subtitle
        this.create_title_and_subtitle(svg);
    }
}