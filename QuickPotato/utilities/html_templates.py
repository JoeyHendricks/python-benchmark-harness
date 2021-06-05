flame_graph_template = """
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">

    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">
    <link rel="stylesheet" type="text/css" href="https://cdn.jsdelivr.net/gh/spiermar/d3-flame-graph@2.0.3/dist/d3-flamegraph.css">
    <script src="https://code.jquery.com/jquery-3.5.1.min.js"></script>

    <style>

    /* Space out content a bit */
    body {
      padding-top: 20px;
      padding-bottom: 20px;
    }

    /* Custom page header */
    .header {
      padding-bottom: 20px;
      padding-right: 15px;
      padding-left: 15px;
      border-bottom: 1px solid #e5e5e5;
    }

    /* Make the masthead heading the same height as the navigation */
    .header h3 {
      margin-top: 0;
      margin-bottom: 0;
      line-height: 40px;
    }

    /* Customize container */
    .container {
      max-width: 990px;
    }
    </style>

    <title>d3-flame-graph</title>

    <!-- HTML5 shim and Respond.js for IE8 support of HTML5 elements and media queries -->
    <!--[if lt IE 9]>
      <script src="https://oss.maxcdn.com/html5shiv/3.7.2/html5shiv.min.js"></script>
      <script src="https://oss.maxcdn.com/respond/1.4.2/respond.min.js"></script>
    <![endif]-->
  </head>
  <body>
    <div class="container">
      <div class="header clearfix">
        <nav>
          <div class="pull-right">
            <form class="form-inline" id="form">
              <select id="sample" class="form-control">
              {% for sample in list_of_samples %}
                <option>{{sample}}</option>
              {% endfor %}
              </select>
              <a class="btn" href="javascript: resetZoom();">Reset zoom</a>
              <a class="btn" href="javascript: clear();">Clear</a>
              <div class="form-group">
                <input type="text" class="form-control" id="term">
              </div>
              <a class="btn btn-primary" href="javascript: search();">Search</a>
            </form>
          </div>
        </nav>
        <h3 class="text-muted">QuickPotato</h3>
      </div>
      <div id="chart">
      </div>
      <hr>
      <div id="details">
      </div>
    </div>

    <!-- D3.js -->
    <script src="https://d3js.org/d3.v4.min.js" charset="utf-8"></script>

    <!-- d3-tip -->
    <script type="text/javascript" src=https://cdnjs.cloudflare.com/ajax/libs/d3-tip/0.9.1/d3-tip.min.js></script>

    <!-- d3-flamegraph -->
    <script type="text/javascript" src="https://cdn.jsdelivr.net/gh/spiermar/d3-flame-graph@2.0.3/dist/d3-flamegraph.min.js"></script>

    <script type="text/javascript">

    var payload = {
    {% for json in payload %}
      '{{json["name"]}}': {{json}},
    {% endfor %}
    };

    var flameGraph = null;

    $(document).ready(function(){
      $(document).ready(render_flame_graph);
      $('#sample').on('change', render_flame_graph);
    });

    document.getElementById("form").addEventListener("submit", function(event){
      event.preventDefault();
      search();
    });

    function search() {
      var term = document.getElementById("term").value;
      flameGraph.search(term);
    }

    function clear() {
      document.getElementById('term').value = '';
      flameGraph.clear();
    }

    function resetZoom() {
      flameGraph.resetZoom();
    }

    function onClick(d) {
      console.info("Clicked on " + d.data.name);
    }

    function render_flame_graph(){

      $("#chart").empty();
      var selected_sample = $('select[id="sample"] option:selected').val()

      flameGraph = d3.flamegraph()
      .width(960)
      .cellHeight(25)
      .transitionDuration(750)
      .minFrameSize(5)
      .transitionEase(d3.easeCubic)
      .sort(true)
      .title("")
      .onClick(onClick)
      .differential(false)
      .selfValue(false);

      var details = document.getElementById("details");
      flameGraph.setDetailsElement(details);

      d3.select("#chart")
      .datum(payload[selected_sample])
      .call(flameGraph);
    }
    </script>
  </body>
</html>
"""

heatmap_template = """
<!DOCTYPE html>
<meta charset="utf-8">

<head>
    <script src="https://d3js.org/d3.v4.js"></script>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta3/dist/css/bootstrap.min.css" 
    rel="stylesheet" integrity="sha384-eOJMYsd53ii+scO/bJGFsiCZc+5NDVN2yr8+0RDqr0Ql0h+rP48ckxlpbzKgwra6" 
    crossorigin="anonymous">
</head>

<body>

    <div class="container-fluid">
        <br>
        <div class="row">
            <div class="col-8">
                <div id="analytics">

                </div>
            </div>
            <div class="col-4">
                <div id="sample" style="margin-right: 10px; margin-top: 75px;">
                    <div class="card" id="meta_data_viewer" style="overflow-y: auto; max-height: 800px;">
                        <div class="card-body">
                            <h5 class="card-title">Click on a box to explore it's information</h5>
                        </div>
                        <ul class="list-group list-group-flush">
                            <li class="list-group-item">Code Path will be displayed here.</li>
                            <li class="list-group-item">Function information will be displayed here.</li>
                            <li class="list-group-item">Parent function information will be displayed here.</li>
                        </ul>
                    </div>
                </div>
            </div>
        </div>
    </div>
</body>

<script>

    var data = {{payload}};
    var TimeScale = {{time_scale}};

    class HeatMap {
        constructor(data, scale) {
            // Extracts the samples and the code paths
            this.data = data;
            this.scale = scale;
            this.heatmap_id = 'QuickPotatoHeatmap';
            this.Samples = d3.map(this.data, d => d.x_axis_identifier_sample_ids).keys();
            this.CodePaths = d3.map(this.data, d => d.y_axis_identifier_parent_child_pair).keys();
            this.Tests = d3.map(this.data, d => d.x_axis_identifier_test_ids).keys();
    
            // Setting the dimensions, margins and the color palette of the graph
            this.margin = { top: 110, right: 10, bottom: 100, left: 75 };
            this.width = 1800 - this.margin.left - this.margin.right;
            this.height = 1300 - this.margin.top - this.margin.bottom;
            this.ColorPalette = ['#f1bc31', '#e9731e', '#e4671f', '#df5a21', '#bc2d23'];
    
            // Adding the heatmap to the analytic section
            document.getElementById("analytics").innerHTML += '<div id="' + this.heatmap_id + '"></div>';
        }
    
        create_tooltip() {
            var tooltip = d3.select("#" + this.heatmap_id)
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
            return function (d) {
                tooltip
                    .style("opacity", 1)
    
                d3.select(this)
                    .style("stroke", "black")
                    .style("opacity", 1)
            }
        }
    
        create_mouse_move_event(tooltip) {
            return function (d) {
                var mouse_position = Math.abs(event.clientX);
                var tooltip_text = 'Test ID: ' + d.x_axis_identifier_test_ids + ' Sample ID:'
                    + d.x_axis_identifier_sample_ids + ' Function '
                    + d.y_axis_identifier_parent_child_pair + ', ran for ' + d.latency;
    
                if (mouse_position > 700) {
                    var tooltip_position = d3.event.pageX - 10 - tooltip.node().getBoundingClientRect().width + "px"
                } else {
                    var tooltip_position = d3.event.pageX + 10 + "px"
                }
    
                tooltip
                    .html(tooltip_text)
                    .style("left", tooltip_position)
                    .style("top", d3.event.pageY + 10 + "px")
            }
        }
    
        create_mouse_leave_event(tooltip) {
            return function (d) {
                tooltip
                    .style("opacity", 0)
                d3.select(this)
                    .style("stroke", "none")
                    .style("opacity", 0.8)
            }
        }
    
        create_mouse_click_event(json) {
            var explorer = document.getElementById("meta_data_viewer")
    
            // Generate human friendly code path
            var code_path = "";
            for (var method of json.predicted_code_path) {
                method = method.replace(/[^\w\s]/gi, '')
                if (method == "Code path could not be predicted.") {
                    var code_path ="Code path could not be predicted."
    
                } else if (code_path == "") {
    
                    var code_path = method;
    
                } else {
    
                    var code_path = code_path + " --> " + method;
                }
            }
            var html = `
                <div class="card-body">
                    <h5 class="card-title">Test Information:</h5>
                    <p class="card-text">
                        Test ID: ${json.x_axis_identifier_test_ids}<br>
                        Sample ID:  ${json.x_axis_identifier_sample_ids}<br>
                    </p>
                </div>
                <ul class="list-group list-group-flush">
                    <li class="list-group-item">
                        <h5 class="card-title">Function Information:</h5>
                        <p class="card-text">
                            name: ${json.y_axis_identifier_parent_child_pair}<br>
                            Time spend: ${json.latency}<br>
                            Number of calls: ${json.meta_data.number_of_calls}<br>
                        </p>
                    </li>
                    <li class="list-group-item">
                        <h5 class="card-title">Detected Code Path</h5>
                        <p class="card-text">${code_path}</p>
                    </li>
                    <li class="list-group-item">
                        <h5 class="card-title">Function location</h5>
                        <p class="card-text">Path: ${json.meta_data.child_path}</p>
                        <p class="card-text">Line Number: ${json.meta_data.child_line_number}</p>
                    </li>
                    <li class="list-group-item">
                        <h5 class="card-title">Parent location</h5>
                        <p class="card-text">Path: ${json.meta_data.parent_path}</p>
                        <p class="card-text">Line Number: ${json.meta_data.parent_line_number}</p>
                    </li>
                </ul>
            `;
    
            explorer.innerHTML = html;
        }
    
        create_color_palette() {
            return d3.scaleLinear()
                .range(this.ColorPalette)
                .domain(this.scale)
        }
    
        create_sample_x_axis(svg, domain) {
            // Build X axis:
            var x_axis = d3.scaleBand()
                .range([0, this.width / this.Tests.length - 10])
                .domain(domain)
                .padding(0.05)
    
            // text label for the x axis
            svg.append("text")
                .attr("x", 870)
                .attr("y", 1120)
                .style("font-size", 30)
                .style("text-anchor", "middle")
                .text("Test id's and samples");
    
            return x_axis
        }
    
        create_tests_x_axis(svg) {
            // Build X axis:
            var axis = d3.scaleBand()
                .range([-30, this.width])
                .domain(this.Tests)
                .padding(0.05)
            return axis;
        }
    
        create_y_axis(svg) {
            var y_axis = d3.scaleBand()
                .range([this.height, 0])
                .domain(this.CodePaths)
                .padding(0.05);
    
            // text label for the y axis
            svg.append("text")
                .attr("x", 550)
                .attr("y", 50)
                .attr("transform", "rotate(90)")
                .style("font-size", 30)
                .style("text-anchor", "middle")
                .text("Code Paths");
    
            return y_axis
    
        }
    
        create_title_and_subtitle(svg) {
    
            var date = new Date().toLocaleDateString();
            var time = new Date().toLocaleTimeString();
    
            // Add title to graph
            svg.append("text")
                .attr("x", 30)
                .attr("y", -70)
                .attr("text-anchor", "left")
                .style("font-size", 50)
                .text("QuickPotato Code Path Heatmap");
    
            // Add subtitle to graph
            svg.append("text")
                .attr("x", 35)
                .attr("y", -35)
                .attr("text-anchor", "left")
                .style("font-size", 25)
                .style("fill", "grey")
                .style("max-width", 400)
                .text('Generated on ' + date + ' ' + time);
        }
    
        render() {
            // Add the svg image to the page and generate the color palette
            var svg = d3.select("#" + this.heatmap_id)
                .append("svg")
                .attr("viewBox", `0 0 1900 1400`)
                .append("g")
                .attr("transform", "translate(" + this.margin.left + "," + this.margin.top + ")");
            var Color = this.create_color_palette();
    
            // Create the mouse and tooltip event handlers
            var tooltip = this.create_tooltip();
            var mouseover = this.create_mouse_over_event(tooltip);
            var mousemove = this.create_mouse_move_event(tooltip);
            var mouseleave = this.create_mouse_leave_event(tooltip);
            var mouseclick = this.create_mouse_click_event;
    
            // Build the X axis for each subplot
            var x_axes = {};
            this.Tests.forEach(test => {
                var data_for_test = this.data.filter(d => d.x_axis_identifier_test_ids === test);
                var samples_for_test = d3.map(data_for_test, d => d.x_axis_identifier_sample_ids).keys();
                x_axes[test] = this.create_sample_x_axis(svg, samples_for_test);
            });
            var test_axis = this.create_tests_x_axis(svg);
    
            // Build the Y axis:
            var y_axis = this.create_y_axis(svg);
    
            // Add all the code paths per sample as squares
            svg.selectAll()
                .data(this.data, d => d.x_axis_identifier_sample_ids + ':' + d.y_axis_identifier_parent_child_pair)
                .enter()
                .append("rect")
                .attr("x", d => {
                    return x_axes[d.x_axis_identifier_test_ids](d.x_axis_identifier_sample_ids) + test_axis(d.x_axis_identifier_test_ids);
                })
                .attr("y", function (d) {
                    return y_axis(d.y_axis_identifier_parent_child_pair)
                })
                .attr("rx", 4)
                .attr("ry", 4)
                .attr("width", d => x_axes[d.x_axis_identifier_test_ids].bandwidth())
                .attr("height", y_axis.bandwidth())
                .style("fill", d => Color(d.latency))
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
    new HeatMap(data, TimeScale).render()
</script>
"""
