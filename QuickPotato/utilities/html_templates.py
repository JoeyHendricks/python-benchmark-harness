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

sample_heatmap_template = """"
<!DOCTYPE html>
<meta charset="utf-8">

<!-- Load d3.js -->
<script src="https://d3js.org/d3.v4.js"></script>

<!-- Create a div where the graph will take place -->
<center>
  <div id="heatmap">
    
  </div>
</center>

<!-- Load color palettes -->
<script src="https://d3js.org/d3-scale-chromatic.v1.min.js"></script>


<script>
    var payload = [{"sample_id": "GL1QNS5H", "path": "say_my_name_and_more", "time": 14.014}, {"sample_id": "GL1QNS5H", "path": "say_my_name_and_more/sleep_based_on_name_length", "time": 14.0139}, {"sample_id": "GL1QNS5H", "path": "say_my_name_and_more/sleep_based_on_name_length/ built in method time sleep", "time": 14.0138}, {"sample_id": "KF19PSAC", "path": "say_my_name_and_more", "time": 14.0135}, {"sample_id": "KF19PSAC", "path": "say_my_name_and_more/sleep_based_on_name_length", "time": 14.0133}, {"sample_id": "KF19PSAC", "path": "say_my_name_and_more/sleep_based_on_name_length/ built in method time sleep", "time": 14.0132}, {"sample_id": "J7MIIB81", "path": "say_my_name_and_more", "time": 14.0126}, {"sample_id": "J7MIIB81", "path": "say_my_name_and_more/sleep_based_on_name_length", "time": 14.0125}, {"sample_id": "J7MIIB81", "path": "say_my_name_and_more/sleep_based_on_name_length/ built in method time sleep", "time": 14.0125}, {"sample_id": "09ELLFYK", "path": "say_my_name_and_more", "time": 14.0124}, {"sample_id": "09ELLFYK", "path": "say_my_name_and_more/sleep_based_on_name_length", "time": 14.0122}, {"sample_id": "09ELLFYK", "path": "say_my_name_and_more/sleep_based_on_name_length/ built in method time sleep", "time": 14.0122}, {"sample_id": "2FQ69V0N", "path": "say_my_name_and_more", "time": 14.0101}, {"sample_id": "2FQ69V0N", "path": "say_my_name_and_more/sleep_based_on_name_length", "time": 14.0099}, {"sample_id": "2FQ69V0N", "path": "say_my_name_and_more/sleep_based_on_name_length/ built in method time sleep", "time": 14.0098}, {"sample_id": "HUFC7K9V", "path": "say_my_name_and_more", "time": 14.0086}, {"sample_id": "HUFC7K9V", "path": "say_my_name_and_more/sleep_based_on_name_length", "time": 14.0084}, {"sample_id": "HUFC7K9V", "path": "say_my_name_and_more/sleep_based_on_name_length/ built in method time sleep", "time": 14.0083}, {"sample_id": "M94AHDHE", "path": "say_my_name_and_more", "time": 14.0053}, {"sample_id": "M94AHDHE", "path": "say_my_name_and_more/sleep_based_on_name_length", "time": 14.0051}, {"sample_id": "M94AHDHE", "path": "say_my_name_and_more/sleep_based_on_name_length/ built in method time sleep", "time": 14.0051}, {"sample_id": "RZE7D9T5", "path": "say_my_name_and_more", "time": 14.0045}, {"sample_id": "RZE7D9T5", "path": "say_my_name_and_more/sleep_based_on_name_length", "time": 14.0044}, {"sample_id": "RZE7D9T5", "path": "say_my_name_and_more/sleep_based_on_name_length/ built in method time sleep", "time": 14.0044}, {"sample_id": "DA5F9J87", "path": "say_my_name_and_more", "time": 14.0022}, {"sample_id": "DA5F9J87", "path": "say_my_name_and_more/sleep_based_on_name_length", "time": 14.002}, {"sample_id": "DA5F9J87", "path": "say_my_name_and_more/sleep_based_on_name_length/ built in method time sleep", "time": 14.002}, {"sample_id": "84E6CUPX", "path": "say_my_name_and_more", "time": 14.0007}, {"sample_id": "84E6CUPX", "path": "say_my_name_and_more/sleep_based_on_name_length", "time": 14.0005}, {"sample_id": "84E6CUPX", "path": "say_my_name_and_more/sleep_based_on_name_length/ built in method time sleep", "time": 14.0005}, {"sample_id": "KF19PSAC", "path": "say_my_name_and_more/ built in method builtins print", "time": 0.0001608}, {"sample_id": "2FQ69V0N", "path": "say_my_name_and_more/ built in method builtins print", "time": 0.0001548}, {"sample_id": "09ELLFYK", "path": "say_my_name_and_more/ built in method builtins print", "time": 0.0001548}, {"sample_id": "HUFC7K9V", "path": "say_my_name_and_more/ built in method builtins print", "time": 0.0001519}, {"sample_id": "M94AHDHE", "path": "say_my_name_and_more/ built in method builtins print", "time": 0.0001511}, {"sample_id": "84E6CUPX", "path": "say_my_name_and_more/ built in method builtins print", "time": 0.0001045}, {"sample_id": "2FQ69V0N", "path": "say_my_name_and_more/length_of_name", "time": 9.93e-05}, {"sample_id": "2FQ69V0N", "path": "say_my_name_and_more/sleep_based_on_name_length/length_of_name", "time": 9.93e-05}, {"sample_id": "09ELLFYK", "path": "say_my_name_and_more/length_of_name", "time": 9.8e-05}, {"sample_id": "09ELLFYK", "path": "say_my_name_and_more/sleep_based_on_name_length/length_of_name", "time": 9.8e-05}, {"sample_id": "HUFC7K9V", "path": "say_my_name_and_more/length_of_name", "time": 9.74e-05}, {"sample_id": "HUFC7K9V", "path": "say_my_name_and_more/sleep_based_on_name_length/length_of_name", "time": 9.74e-05}, {"sample_id": "KF19PSAC", "path": "say_my_name_and_more/length_of_name", "time": 9.72e-05}, {"sample_id": "KF19PSAC", "path": "say_my_name_and_more/sleep_based_on_name_length/length_of_name", "time": 9.72e-05}, {"sample_id": "M94AHDHE", "path": "say_my_name_and_more/length_of_name", "time": 9.57e-05}, {"sample_id": "M94AHDHE", "path": "say_my_name_and_more/sleep_based_on_name_length/length_of_name", "time": 9.57e-05}, {"sample_id": "DA5F9J87", "path": "say_my_name_and_more/ built in method builtins print", "time": 8.82e-05}, {"sample_id": "2FQ69V0N", "path": "say_my_name_and_more/sleep_based_on_name_length/length_of_name/show_message_when_name_very_long", "time": 8.73e-05}, {"sample_id": "2FQ69V0N", "path": "say_my_name_and_more/length_of_name/show_message_when_name_very_long", "time": 8.73e-05}, {"sample_id": "GL1QNS5H", "path": "say_my_name_and_more/ built in method builtins print", "time": 8.57e-05}, {"sample_id": "HUFC7K9V", "path": "say_my_name_and_more/sleep_based_on_name_length/length_of_name/show_message_when_name_very_long", "time": 8.57e-05}, {"sample_id": "HUFC7K9V", "path": "say_my_name_and_more/length_of_name/show_message_when_name_very_long", "time": 8.57e-05}, {"sample_id": "09ELLFYK", "path": "say_my_name_and_more/sleep_based_on_name_length/length_of_name/show_message_when_name_very_long", "time": 8.53e-05}, {"sample_id": "09ELLFYK", "path": "say_my_name_and_more/length_of_name/show_message_when_name_very_long", "time": 8.53e-05}, {"sample_id": "KF19PSAC", "path": "say_my_name_and_more/sleep_based_on_name_length/length_of_name/show_message_when_name_very_long", "time": 8.38e-05}, {"sample_id": "KF19PSAC", "path": "say_my_name_and_more/length_of_name/show_message_when_name_very_long", "time": 8.38e-05}, {"sample_id": "M94AHDHE", "path": "say_my_name_and_more/sleep_based_on_name_length/length_of_name/show_message_when_name_very_long", "time": 8.35e-05}, {"sample_id": "M94AHDHE", "path": "say_my_name_and_more/length_of_name/show_message_when_name_very_long", "time": 8.35e-05}, {"sample_id": "J7MIIB81", "path": "say_my_name_and_more/ built in method builtins print", "time": 8.35e-05}, {"sample_id": "RZE7D9T5", "path": "say_my_name_and_more/ built in method builtins print", "time": 6.83e-05}, {"sample_id": "84E6CUPX", "path": "say_my_name_and_more/length_of_name", "time": 6.7e-05}, {"sample_id": "84E6CUPX", "path": "say_my_name_and_more/sleep_based_on_name_length/length_of_name", "time": 6.7e-05}, {"sample_id": "84E6CUPX", "path": "say_my_name_and_more/sleep_based_on_name_length/length_of_name/show_message_when_name_very_long", "time": 5.85e-05}, {"sample_id": "84E6CUPX", "path": "say_my_name_and_more/length_of_name/show_message_when_name_very_long", "time": 5.85e-05}, {"sample_id": "DA5F9J87", "path": "say_my_name_and_more/length_of_name", "time": 5.35e-05}, {"sample_id": "DA5F9J87", "path": "say_my_name_and_more/sleep_based_on_name_length/length_of_name", "time": 5.35e-05}, {"sample_id": "GL1QNS5H", "path": "say_my_name_and_more/length_of_name", "time": 5.31e-05}, {"sample_id": "GL1QNS5H", "path": "say_my_name_and_more/sleep_based_on_name_length/length_of_name", "time": 5.31e-05}, {"sample_id": "J7MIIB81", "path": "say_my_name_and_more/length_of_name", "time": 5.22e-05}, {"sample_id": "J7MIIB81", "path": "say_my_name_and_more/sleep_based_on_name_length/length_of_name", "time": 5.22e-05}, {"sample_id": "DA5F9J87", "path": "say_my_name_and_more/sleep_based_on_name_length/length_of_name/show_message_when_name_very_long", "time": 4.66e-05}, {"sample_id": "DA5F9J87", "path": "say_my_name_and_more/length_of_name/show_message_when_name_very_long", "time": 4.66e-05}, {"sample_id": "HUFC7K9V", "path": "say_my_name_and_more/sleep_based_on_name_length/ built in method time sleep/ length_of_name/show_message_when_name_very_long/x", "time": 4.63e-05}, {"sample_id": "HUFC7K9V", "path": "say_my_name_and_more/sleep_based_on_name_length/ built in method time sleep/ length_of_name/show_message_when_name_very_long/x", "time": 4.63e-05}, {"sample_id": "GL1QNS5H", "path": "say_my_name_and_more/sleep_based_on_name_length/length_of_name/show_message_when_name_very_long", "time": 4.62e-05}, {"sample_id": "GL1QNS5H", "path": "say_my_name_and_more/length_of_name/show_message_when_name_very_long", "time": 4.62e-05}, {"sample_id": "2FQ69V0N", "path": "say_my_name_and_more/sleep_based_on_name_length/ built in method time sleep/ length_of_name/show_message_when_name_very_long/x", "time": 4.6e-05}, {"sample_id": "2FQ69V0N", "path": "say_my_name_and_more/sleep_based_on_name_length/ built in method time sleep/ length_of_name/show_message_when_name_very_long/x", "time": 4.6e-05}, {"sample_id": "J7MIIB81", "path": "say_my_name_and_more/sleep_based_on_name_length/length_of_name/show_message_when_name_very_long", "time": 4.53e-05}, {"sample_id": "J7MIIB81", "path": "say_my_name_and_more/length_of_name/show_message_when_name_very_long", "time": 4.53e-05}, {"sample_id": "09ELLFYK", "path": "say_my_name_and_more/sleep_based_on_name_length/ built in method time sleep/ length_of_name/show_message_when_name_very_long/x", "time": 4.46e-05}, {"sample_id": "09ELLFYK", "path": "say_my_name_and_more/sleep_based_on_name_length/ built in method time sleep/ length_of_name/show_message_when_name_very_long/x", "time": 4.46e-05}, {"sample_id": "KF19PSAC", "path": "say_my_name_and_more/sleep_based_on_name_length/ built in method time sleep/ length_of_name/show_message_when_name_very_long/x", "time": 4.4e-05}, {"sample_id": "KF19PSAC", "path": "say_my_name_and_more/sleep_based_on_name_length/ built in method time sleep/ length_of_name/show_message_when_name_very_long/x", "time": 4.4e-05}, {"sample_id": "M94AHDHE", "path": "say_my_name_and_more/sleep_based_on_name_length/ built in method time sleep/ length_of_name/show_message_when_name_very_long/x", "time": 4.37e-05}, {"sample_id": "M94AHDHE", "path": "say_my_name_and_more/sleep_based_on_name_length/ built in method time sleep/ length_of_name/show_message_when_name_very_long/x", "time": 4.37e-05}, {"sample_id": "RZE7D9T5", "path": "say_my_name_and_more/length_of_name", "time": 4.31e-05}, {"sample_id": "RZE7D9T5", "path": "say_my_name_and_more/sleep_based_on_name_length/length_of_name", "time": 4.31e-05}, {"sample_id": "HUFC7K9V", "path": "say_my_name_and_more/sleep_based_on_name_length/ built in method time sleep/ length_of_name/show_message_when_name_very_long/x/y", "time": 4.16e-05}, {"sample_id": "HUFC7K9V", "path": "say_my_name_and_more/sleep_based_on_name_length/ built in method time sleep/ length_of_name/show_message_when_name_very_long/x/y", "time": 4.16e-05}, {"sample_id": "2FQ69V0N", "path": "say_my_name_and_more/sleep_based_on_name_length/ built in method time sleep/ length_of_name/show_message_when_name_very_long/x/y", "time": 4.11e-05}, {"sample_id": "2FQ69V0N", "path": "say_my_name_and_more/sleep_based_on_name_length/ built in method time sleep/ length_of_name/show_message_when_name_very_long/x/y", "time": 4.11e-05}, {"sample_id": "09ELLFYK", "path": "say_my_name_and_more/sleep_based_on_name_length/ built in method time sleep/ length_of_name/show_message_when_name_very_long/x/y", "time": 3.98e-05}, {"sample_id": "09ELLFYK", "path": "say_my_name_and_more/sleep_based_on_name_length/ built in method time sleep/ length_of_name/show_message_when_name_very_long/x/y", "time": 3.98e-05}, {"sample_id": "KF19PSAC", "path": "say_my_name_and_more/sleep_based_on_name_length/ built in method time sleep/ length_of_name/show_message_when_name_very_long/x/y", "time": 3.96e-05}, {"sample_id": "KF19PSAC", "path": "say_my_name_and_more/sleep_based_on_name_length/ built in method time sleep/ length_of_name/show_message_when_name_very_long/x/y", "time": 3.96e-05}, {"sample_id": "M94AHDHE", "path": "say_my_name_and_more/sleep_based_on_name_length/ built in method time sleep/ length_of_name/show_message_when_name_very_long/x/y", "time": 3.93e-05}, {"sample_id": "M94AHDHE", "path": "say_my_name_and_more/sleep_based_on_name_length/ built in method time sleep/ length_of_name/show_message_when_name_very_long/x/y", "time": 3.93e-05}, {"sample_id": "RZE7D9T5", "path": "say_my_name_and_more/sleep_based_on_name_length/length_of_name/show_message_when_name_very_long", "time": 3.75e-05}, {"sample_id": "RZE7D9T5", "path": "say_my_name_and_more/length_of_name/show_message_when_name_very_long", "time": 3.75e-05}, {"sample_id": "84E6CUPX", "path": "say_my_name_and_more/sleep_based_on_name_length/ built in method time sleep/ length_of_name/show_message_when_name_very_long/x", "time": 3.02e-05}, {"sample_id": "84E6CUPX", "path": "say_my_name_and_more/sleep_based_on_name_length/ built in method time sleep/ length_of_name/show_message_when_name_very_long/x", "time": 3.02e-05}, {"sample_id": "84E6CUPX", "path": "say_my_name_and_more/sleep_based_on_name_length/ built in method time sleep/ length_of_name/show_message_when_name_very_long/x/y", "time": 2.71e-05}, {"sample_id": "84E6CUPX", "path": "say_my_name_and_more/sleep_based_on_name_length/ built in method time sleep/ length_of_name/show_message_when_name_very_long/x/y", "time": 2.71e-05}, {"sample_id": "DA5F9J87", "path": "say_my_name_and_more/sleep_based_on_name_length/ built in method time sleep/ length_of_name/show_message_when_name_very_long/x", "time": 2.52e-05}, {"sample_id": "DA5F9J87", "path": "say_my_name_and_more/sleep_based_on_name_length/ built in method time sleep/ length_of_name/show_message_when_name_very_long/x", "time": 2.52e-05}, {"sample_id": "GL1QNS5H", "path": "say_my_name_and_more/sleep_based_on_name_length/ built in method time sleep/ length_of_name/show_message_when_name_very_long/x", "time": 2.45e-05}, {"sample_id": "GL1QNS5H", "path": "say_my_name_and_more/sleep_based_on_name_length/ built in method time sleep/ length_of_name/show_message_when_name_very_long/x", "time": 2.45e-05}, {"sample_id": "J7MIIB81", "path": "say_my_name_and_more/sleep_based_on_name_length/ built in method time sleep/ length_of_name/show_message_when_name_very_long/x", "time": 2.42e-05}, {"sample_id": "J7MIIB81", "path": "say_my_name_and_more/sleep_based_on_name_length/ built in method time sleep/ length_of_name/show_message_when_name_very_long/x", "time": 2.42e-05}, {"sample_id": "DA5F9J87", "path": "say_my_name_and_more/sleep_based_on_name_length/ built in method time sleep/ length_of_name/show_message_when_name_very_long/x/y", "time": 2.2e-05}, {"sample_id": "DA5F9J87", "path": "say_my_name_and_more/sleep_based_on_name_length/ built in method time sleep/ length_of_name/show_message_when_name_very_long/x/y", "time": 2.2e-05}, {"sample_id": "GL1QNS5H", "path": "say_my_name_and_more/sleep_based_on_name_length/ built in method time sleep/ length_of_name/show_message_when_name_very_long/x/y", "time": 2.2e-05}, {"sample_id": "GL1QNS5H", "path": "say_my_name_and_more/sleep_based_on_name_length/ built in method time sleep/ length_of_name/show_message_when_name_very_long/x/y", "time": 2.2e-05}, {"sample_id": "J7MIIB81", "path": "say_my_name_and_more/sleep_based_on_name_length/ built in method time sleep/ length_of_name/show_message_when_name_very_long/x/y", "time": 2.15e-05}, {"sample_id": "J7MIIB81", "path": "say_my_name_and_more/sleep_based_on_name_length/ built in method time sleep/ length_of_name/show_message_when_name_very_long/x/y", "time": 2.15e-05}, {"sample_id": "RZE7D9T5", "path": "say_my_name_and_more/sleep_based_on_name_length/ built in method time sleep/ length_of_name/show_message_when_name_very_long/x", "time": 1.98e-05}, {"sample_id": "RZE7D9T5", "path": "say_my_name_and_more/sleep_based_on_name_length/ built in method time sleep/ length_of_name/show_message_when_name_very_long/x", "time": 1.98e-05}, {"sample_id": "KF19PSAC", "path": "say_my_name_and_more/capitalize_name", "time": 1.83e-05}, {"sample_id": "RZE7D9T5", "path": "say_my_name_and_more/sleep_based_on_name_length/ built in method time sleep/ length_of_name/show_message_when_name_very_long/x/y", "time": 1.77e-05}, {"sample_id": "RZE7D9T5", "path": "say_my_name_and_more/sleep_based_on_name_length/ built in method time sleep/ length_of_name/show_message_when_name_very_long/x/y", "time": 1.77e-05}, {"sample_id": "DA5F9J87", "path": "say_my_name_and_more/capitalize_name", "time": 1.68e-05}, {"sample_id": "09ELLFYK", "path": "say_my_name_and_more/capitalize_name", "time": 1.24e-05}, {"sample_id": "M94AHDHE", "path": "say_my_name_and_more/capitalize_name", "time": 1.18e-05}, {"sample_id": "2FQ69V0N", "path": "say_my_name_and_more/capitalize_name", "time": 1.17e-05}, {"sample_id": "HUFC7K9V", "path": "say_my_name_and_more/capitalize_name", "time": 1.15e-05}, {"sample_id": "84E6CUPX", "path": "say_my_name_and_more/capitalize_name", "time": 8.8e-06}, {"sample_id": "GL1QNS5H", "path": "say_my_name_and_more/capitalize_name", "time": 7.5e-06}, {"sample_id": "J7MIIB81", "path": "say_my_name_and_more/capitalize_name", "time": 6.9e-06}, {"sample_id": "2FQ69V0N", "path": "say_my_name_and_more/lowercase_name", "time": 6.8e-06}, {"sample_id": "HUFC7K9V", "path": "say_my_name_and_more/lowercase_name", "time": 6.6e-06}, {"sample_id": "09ELLFYK", "path": "say_my_name_and_more/lowercase_name", "time": 6.6e-06}, {"sample_id": "M94AHDHE", "path": "say_my_name_and_more/lowercase_name", "time": 6.5e-06}, {"sample_id": "KF19PSAC", "path": "say_my_name_and_more/lowercase_name", "time": 6.2e-06}, {"sample_id": "RZE7D9T5", "path": "say_my_name_and_more/capitalize_name", "time": 5.7e-06}, {"sample_id": "KF19PSAC", "path": "say_my_name_and_more/uppercase_name", "time": 5.5e-06}, {"sample_id": "HUFC7K9V", "path": "say_my_name_and_more/uppercase_name", "time": 5.1e-06}, {"sample_id": "M94AHDHE", "path": "say_my_name_and_more/uppercase_name", "time": 5e-06}, {"sample_id": "2FQ69V0N", "path": "say_my_name_and_more/uppercase_name", "time": 4.9e-06}, {"sample_id": "09ELLFYK", "path": "say_my_name_and_more/uppercase_name", "time": 4.8e-06}, {"sample_id": "84E6CUPX", "path": "say_my_name_and_more/lowercase_name", "time": 4.6e-06}, {"sample_id": "KF19PSAC", "path": "say_my_name_and_more/capitalize_name/ method  capitalize  of  str  objects", "time": 4.1e-06}, {"sample_id": "GL1QNS5H", "path": "say_my_name_and_more/lowercase_name", "time": 3.9e-06}, {"sample_id": "DA5F9J87", "path": "say_my_name_and_more/lowercase_name", "time": 3.8e-06}, {"sample_id": "84E6CUPX", "path": "say_my_name_and_more/uppercase_name", "time": 3.6e-06}, {"sample_id": "J7MIIB81", "path": "say_my_name_and_more/lowercase_name", "time": 3.6e-06}, {"sample_id": "J7MIIB81", "path": "say_my_name_and_more/uppercase_name", "time": 3.1e-06}, {"sample_id": "GL1QNS5H", "path": "say_my_name_and_more/uppercase_name", "time": 3e-06}, {"sample_id": "DA5F9J87", "path": "say_my_name_and_more/uppercase_name", "time": 2.9e-06}, {"sample_id": "2FQ69V0N", "path": "say_my_name_and_more/capitalize_name/ method  capitalize  of  str  objects", "time": 2.9e-06}, {"sample_id": "09ELLFYK", "path": "say_my_name_and_more/capitalize_name/ method  capitalize  of  str  objects", "time": 2.9e-06}, {"sample_id": "RZE7D9T5", "path": "say_my_name_and_more/lowercase_name", "time": 2.8e-06}, {"sample_id": "M94AHDHE", "path": "say_my_name_and_more/capitalize_name/ method  capitalize  of  str  objects", "time": 2.8e-06}, {"sample_id": "HUFC7K9V", "path": "say_my_name_and_more/capitalize_name/ method  capitalize  of  str  objects", "time": 2.8e-06}, {"sample_id": "RZE7D9T5", "path": "say_my_name_and_more/uppercase_name", "time": 2.5e-06}, {"sample_id": "84E6CUPX", "path": "say_my_name_and_more/capitalize_name/ method  capitalize  of  str  objects", "time": 2.1e-06}, {"sample_id": "GL1QNS5H", "path": "say_my_name_and_more/capitalize_name/ method  capitalize  of  str  objects", "time": 2e-06}, {"sample_id": "DA5F9J87", "path": "say_my_name_and_more/capitalize_name/ method  capitalize  of  str  objects", "time": 1.9e-06}, {"sample_id": "2FQ69V0N", "path": "say_my_name_and_more/sleep_based_on_name_length/ built in method time sleep/ length_of_name/show_message_when_name_very_long/x/y/foo", "time": 1.8e-06}, {"sample_id": "2FQ69V0N", "path": "say_my_name_and_more/sleep_based_on_name_length/ built in method time sleep/ length_of_name/show_message_when_name_very_long/x/y/foo", "time": 1.8e-06}, {"sample_id": "09ELLFYK", "path": "say_my_name_and_more/sleep_based_on_name_length/length_of_name/ built in method builtins len", "time": 1.7e-06}, {"sample_id": "09ELLFYK", "path": "say_my_name_and_more/length_of_name/ built in method builtins len", "time": 1.7e-06}, {"sample_id": "J7MIIB81", "path": "say_my_name_and_more/capitalize_name/ method  capitalize  of  str  objects", "time": 1.6e-06}, {"sample_id": "M94AHDHE", "path": "say_my_name_and_more/sleep_based_on_name_length/ built in method time sleep/ length_of_name/show_message_when_name_very_long/x/y/foo", "time": 1.5e-06}, {"sample_id": "M94AHDHE", "path": "say_my_name_and_more/sleep_based_on_name_length/ built in method time sleep/ length_of_name/show_message_when_name_very_long/x/y/foo", "time": 1.5e-06}, {"sample_id": "RZE7D9T5", "path": "say_my_name_and_more/capitalize_name/ method  capitalize  of  str  objects", "time": 1.4e-06}, {"sample_id": "KF19PSAC", "path": "say_my_name_and_more/sleep_based_on_name_length/length_of_name/ built in method builtins len", "time": 1.4e-06}, {"sample_id": "KF19PSAC", "path": "say_my_name_and_more/length_of_name/ built in method builtins len", "time": 1.4e-06}, {"sample_id": "M94AHDHE", "path": "say_my_name_and_more/sleep_based_on_name_length/length_of_name/ built in method builtins len", "time": 1.4e-06}, {"sample_id": "M94AHDHE", "path": "say_my_name_and_more/length_of_name/ built in method builtins len", "time": 1.4e-06}, {"sample_id": "HUFC7K9V", "path": "say_my_name_and_more/sleep_based_on_name_length/ built in method time sleep/ length_of_name/show_message_when_name_very_long/x/y/foo", "time": 1.4e-06}, {"sample_id": "HUFC7K9V", "path": "say_my_name_and_more/sleep_based_on_name_length/ built in method time sleep/ length_of_name/show_message_when_name_very_long/x/y/foo", "time": 1.4e-06}, {"sample_id": "09ELLFYK", "path": "say_my_name_and_more/sleep_based_on_name_length/ built in method time sleep/ length_of_name/show_message_when_name_very_long/x/y/foo", "time": 1.4e-06}, {"sample_id": "09ELLFYK", "path": "say_my_name_and_more/sleep_based_on_name_length/ built in method time sleep/ length_of_name/show_message_when_name_very_long/x/y/foo", "time": 1.4e-06}, {"sample_id": "2FQ69V0N", "path": "say_my_name_and_more/sleep_based_on_name_length/length_of_name/ built in method builtins len", "time": 1.3e-06}, {"sample_id": "2FQ69V0N", "path": "say_my_name_and_more/length_of_name/ built in method builtins len", "time": 1.3e-06}, {"sample_id": "KF19PSAC", "path": "say_my_name_and_more/uppercase_name/ method  upper  of  str  objects", "time": 1.3e-06}, {"sample_id": "HUFC7K9V", "path": "say_my_name_and_more/sleep_based_on_name_length/length_of_name/ built in method builtins len", "time": 1.3e-06}, {"sample_id": "HUFC7K9V", "path": "say_my_name_and_more/length_of_name/ built in method builtins len", "time": 1.3e-06}, {"sample_id": "KF19PSAC", "path": "say_my_name_and_more/sleep_based_on_name_length/ built in method time sleep/ length_of_name/show_message_when_name_very_long/x/y/foo", "time": 1.2e-06}, {"sample_id": "KF19PSAC", "path": "say_my_name_and_more/sleep_based_on_name_length/ built in method time sleep/ length_of_name/show_message_when_name_very_long/x/y/foo", "time": 1.2e-06}, {"sample_id": "KF19PSAC", "path": "say_my_name_and_more/lowercase_name/ method  lower  of  str  objects", "time": 1e-06}, {"sample_id": "M94AHDHE", "path": "say_my_name_and_more/uppercase_name/ method  upper  of  str  objects", "time": 1e-06}, {"sample_id": "J7MIIB81", "path": "say_my_name_and_more/sleep_based_on_name_length/ built in method time sleep/ length_of_name/show_message_when_name_very_long/x/y/foo", "time": 1e-06}, {"sample_id": "J7MIIB81", "path": "say_my_name_and_more/sleep_based_on_name_length/ built in method time sleep/ length_of_name/show_message_when_name_very_long/x/y/foo", "time": 1e-06}, {"sample_id": "GL1QNS5H", "path": "say_my_name_and_more/sleep_based_on_name_length/length_of_name/ built in method builtins len", "time": 9e-07}, {"sample_id": "GL1QNS5H", "path": "say_my_name_and_more/sleep_based_on_name_length/ built in method time sleep/ length_of_name/show_message_when_name_very_long/x/y/foo", "time": 9e-07}, {"sample_id": "GL1QNS5H", "path": "say_my_name_and_more/length_of_name/ built in method builtins len", "time": 9e-07}, {"sample_id": "GL1QNS5H", "path": "say_my_name_and_more/sleep_based_on_name_length/ built in method time sleep/ length_of_name/show_message_when_name_very_long/x/y/foo", "time": 9e-07}, {"sample_id": "2FQ69V0N", "path": "say_my_name_and_more/uppercase_name/ method  upper  of  str  objects", "time": 9e-07}, {"sample_id": "09ELLFYK", "path": "say_my_name_and_more/lowercase_name/ method  lower  of  str  objects", "time": 9e-07}, {"sample_id": "09ELLFYK", "path": "say_my_name_and_more/uppercase_name/ method  upper  of  str  objects", "time": 9e-07}, {"sample_id": "84E6CUPX", "path": "say_my_name_and_more/sleep_based_on_name_length/ built in method time sleep/ length_of_name/show_message_when_name_very_long/x/y/foo", "time": 9e-07}, {"sample_id": "84E6CUPX", "path": "say_my_name_and_more/sleep_based_on_name_length/ built in method time sleep/ length_of_name/show_message_when_name_very_long/x/y/foo", "time": 9e-07}, {"sample_id": "DA5F9J87", "path": "say_my_name_and_more/sleep_based_on_name_length/length_of_name/ built in method builtins len", "time": 8e-07}, {"sample_id": "DA5F9J87", "path": "say_my_name_and_more/length_of_name/ built in method builtins len", "time": 8e-07}, {"sample_id": "2FQ69V0N", "path": "say_my_name_and_more/lowercase_name/ method  lower  of  str  objects", "time": 8e-07}, {"sample_id": "M94AHDHE", "path": "say_my_name_and_more/lowercase_name/ method  lower  of  str  objects", "time": 8e-07}, {"sample_id": "HUFC7K9V", "path": "say_my_name_and_more/lowercase_name/ method  lower  of  str  objects", "time": 8e-07}, {"sample_id": "HUFC7K9V", "path": "say_my_name_and_more/uppercase_name/ method  upper  of  str  objects", "time": 8e-07}, {"sample_id": "84E6CUPX", "path": "say_my_name_and_more/sleep_based_on_name_length/length_of_name/ built in method builtins len", "time": 8e-07}, {"sample_id": "84E6CUPX", "path": "say_my_name_and_more/length_of_name/ built in method builtins len", "time": 8e-07}, {"sample_id": "DA5F9J87", "path": "say_my_name_and_more/sleep_based_on_name_length/ built in method time sleep/ length_of_name/show_message_when_name_very_long/x/y/foo", "time": 7e-07}, {"sample_id": "DA5F9J87", "path": "say_my_name_and_more/sleep_based_on_name_length/ built in method time sleep/ length_of_name/show_message_when_name_very_long/x/y/foo", "time": 7e-07}, {"sample_id": "RZE7D9T5", "path": "say_my_name_and_more/sleep_based_on_name_length/ built in method time sleep/ length_of_name/show_message_when_name_very_long/x/y/foo", "time": 7e-07}, {"sample_id": "RZE7D9T5", "path": "say_my_name_and_more/sleep_based_on_name_length/ built in method time sleep/ length_of_name/show_message_when_name_very_long/x/y/foo", "time": 7e-07}, {"sample_id": "84E6CUPX", "path": "say_my_name_and_more/uppercase_name/ method  upper  of  str  objects", "time": 7e-07}, {"sample_id": "J7MIIB81", "path": "say_my_name_and_more/sleep_based_on_name_length/length_of_name/ built in method builtins len", "time": 7e-07}, {"sample_id": "J7MIIB81", "path": "say_my_name_and_more/length_of_name/ built in method builtins len", "time": 7e-07}, {"sample_id": "GL1QNS5H", "path": "say_my_name_and_more/uppercase_name/ method  upper  of  str  objects", "time": 6e-07}, {"sample_id": "RZE7D9T5", "path": "say_my_name_and_more/sleep_based_on_name_length/length_of_name/ built in method builtins len", "time": 6e-07}, {"sample_id": "RZE7D9T5", "path": "say_my_name_and_more/length_of_name/ built in method builtins len", "time": 6e-07}, {"sample_id": "84E6CUPX", "path": "say_my_name_and_more/lowercase_name/ method  lower  of  str  objects", "time": 6e-07}, {"sample_id": "J7MIIB81", "path": "say_my_name_and_more/uppercase_name/ method  upper  of  str  objects", "time": 6e-07}, {"sample_id": "DA5F9J87", "path": "say_my_name_and_more/lowercase_name/ method  lower  of  str  objects", "time": 5e-07}, {"sample_id": "DA5F9J87", "path": "say_my_name_and_more/uppercase_name/ method  upper  of  str  objects", "time": 5e-07}, {"sample_id": "GL1QNS5H", "path": "say_my_name_and_more/lowercase_name/ method  lower  of  str  objects", "time": 4e-07}, {"sample_id": "RZE7D9T5", "path": "say_my_name_and_more/uppercase_name/ method  upper  of  str  objects", "time": 4e-07}, {"sample_id": "J7MIIB81", "path": "say_my_name_and_more/lowercase_name/ method  lower  of  str  objects", "time": 4e-07}, {"sample_id": "RZE7D9T5", "path": "say_my_name_and_more/lowercase_name/ method  lower  of  str  objects", "time": 3e-07}];
    var TimeScale = [1e-07, 3.4199518933533896e-05, 0.011696070952851459, 4.0]

    class HeatMap{
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
            this.Samples = d3.map(this.data, function(d){return d.sample_id;}).keys()
            this.CodePaths = d3.map(this.data, function(d){return d.path;}).keys()

            // Setting the dimensions, margins and the color palette of the graph
            this.margin = {top: 100, right: 100, bottom: 100, left: 100};
            this.width = 2000 - this.margin.left - this.margin.right;
            this.height = 800 - this.margin.top - this.margin.bottom;
            this.ColorPalette = ["#ffe808", "#ffce00", "#ff9a00", "#ff5a00", "#ff0000"]

        }

    render() {
            /*
            The code below will change
            the heading with id = "myH"
            and the paragraph with id = "myP"
            in my web page:
            */

            // add the svg image to the page:
            var svg = d3.select("#heatmap")
                .append("svg")
                .attr("viewBox", `0 0 2000 900`)
            .append("g")
                .attr("transform", "translate(" + this.margin.left + "," + this.margin.top + ")");

            // create a tooltip
            var tooltip = d3.select("#heatmap")
                .append("div")
                .style("opacity", 0)
                .attr("class", "tooltip")
                .style("background-color", "white")
                .style("border", "solid")
                .style("border-width", "2px")
                .style("border-radius", "5px")
                .style("padding", "5px")

            // Three function that change the tooltip when user hover / move / leave a cell
            var mouseover = function(d) {
                tooltip
                    .style("opacity", 1)
                d3.select(this)
                    .style("stroke", "black")
                    .style("opacity", 1)
            }
            var mousemove = function(d) {
                tooltip
                    .html(d.path + " " + d.time)
                    .style("left", (d3.mouse(this)[0]+70) + "px")
                    .style("top", (d3.mouse(this)[1]) + "px")
                }

            var mouseleave = function(d) {
                tooltip
                    .style("opacity", 0)
                    d3.select(this)
                    .style("stroke", "none")
                    .style("opacity", 0.8)
            }

            var Color = d3.scaleLinear()
                .range(this.ColorPalette)
                .domain(this.scale)

            // Build X axis:
            var x_axis = d3.scaleBand()
                .range([ 0, this.width ])
                .domain(this.Samples)
                .padding(0.05);
            svg.append("g")
                .style("font-size", 15)
                .attr("transform", "translate(0," + (this.height) + ")")
                .call(d3.axisBottom(x_axis))
                .selectAll("text")
                    .attr("y", 10)
                    .attr("x", 10)
                    .attr("dy", ".35em")
                    .attr("transform", "rotate(60)")
                    .style("text-anchor", "start");

            // Build Y axis:
            var y_axis = d3.scaleBand()
                .range([ this.height, 0 ])
                .domain(this.CodePaths)
                .padding(0.05);
                svg.append("g")
                    .select(".domain").remove()

            // add the squares
            svg.selectAll()
                .data(this.data, function(d) {return d.sample_id+':'+d.path;})
                .enter()
                .append("rect")
                    .attr("x", function(d) { return x_axis(d.sample_id) })
                    .attr("y", function(d) { return y_axis(d.path) })
                    .attr("rx", 4)
                    .attr("ry", 4)
                    .attr("width", x_axis.bandwidth() )
                    .attr("height", y_axis.bandwidth() )
                    .style("fill", function(d) { return Color(d.time)} )
                    .style("stroke-width", 4)
                    .style("stroke", "none")
                    .style("opacity", 0.8)
                    .on("mouseover", mouseover)
                    .on("mousemove", mousemove)
                    .on("mouseleave", mouseleave)
        }
    }
    const graph = new HeatMap(payload, TimeScale)
    graph.render()
    
    
</script>
"""
