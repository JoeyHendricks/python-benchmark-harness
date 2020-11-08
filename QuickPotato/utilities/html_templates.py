html_svg_header = """
<svg
width='{}'
height='{}'
viewBox='0 0 {} {}'
version='1.1'
xmlns='http://www.w3.org/2000/svg'
xmlns:xlink='http://www.w3.org/1999/xlink'>"""

html_svg_frame = """
<svg class="func_g" x="{x_position}" y="{y_position}" width="{width}" height="25">
<g>
    <title>{function_name} {path} {cumulative_time}</title>
    <rect height="100%" width="100%" fill="rgb{color}" rx="2" ry="2" />
    <text alignment-baseline="central" x="4.0" y="12.0" font-size="12px" fill="rgb(0,0,0)">{function_name}</text>
</g>
</svg>"""

html_test_report = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>QuickPotato</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.5.3/dist/css/bootstrap.min.css"
          integrity="sha384-TX8t27EcRE3e/ihU7zmQxVncDAy5uIKz4rEkgIXeMed4M0jlfIDPvg6uqKI2xXr2" crossorigin="anonymous">
</head>
<script src="https://code.jquery.com/jquery-3.5.1.min.js"></script>
<script type="text/javascript">

function hide_all_unused_objects(){
    // Will hide the unselected benchmark doodle
    var unselected_benchmark_options = $('#benchmark_sample_id option:not(:selected)');
    $.each(unselected_benchmark_options, function( index, value ) {
        flame_graph_sample_id = value["value"]
        $('#' + flame_graph_sample_id).hide();
    });
    // Will hide the unselected baseline doodle
    var unselected_benchmark_options = $('#baseline_sample_id option:not(:selected)');
    $.each(unselected_benchmark_options, function( index, value ) {
        flame_graph_sample_id = value["value"]
        $('#' + flame_graph_sample_id).hide();
    });
}

function show_selected_object(){
    // Will make visible the selected benchmark flame graph
    var selected_benchmark_option_value = $('select[id="benchmark_sample_id"] option:selected').val();
    $('#' + selected_benchmark_option_value).show();
    
    // Will make visible the selected baseline flame graph
    var selected_baseline_option_value = $('select[id="baseline_sample_id"] option:selected').val();
    $('#' + selected_baseline_option_value).show();

// Hide all the old stuff
hide_all_unused_objects();  
}

$(document).ready(function(){
    $(document).ready(hide_all_unused_objects);
    $('#benchmark_sample_id').on('change', hide_all_unused_objects, show_selected_object);
    $('#baseline_sample_id').on('change', hide_all_unused_objects, show_selected_object);
});
</script>
<body>
    <div class="container-fluid">
        <div class="row">
            <div class="col-6">
                <br>
                <p class="d-flex justify-content-center">Benchmark: {{benchmark_test_id}}</p>
                <div class="d-flex justify-content-center">
                    <select id="benchmark_sample_id" name="benchmark_sample_id">
                        {% for item in benchmark_meta_data %}
                        <option value="{{item.sample_id}}">
                        {{item.human_timestamp}} - {{item.name_of_method_under_test}}, {{item.total_response_time}} Sec
                        </option>
                        {% endfor %}
                    </select>
                </div>
            </div>
            <div class="col-6">
                <br>
                <p class="d-flex justify-content-center">Baseline: {{baseline_test_id}}</p>
                <div class="d-flex justify-content-center">
                    <select id="baseline_sample_id" name="baseline_sample_id">
                        {% for item in baseline_meta_data %}
                        <option value="{{item.sample_id}}">
                        {{item.human_timestamp}} - {{item.name_of_method_under_test}}, {{item.total_response_time}} Sec
                        </option>
                        {% endfor %}
                    </select>
                </div>
            </div>
        </div>
        <div class="row">
            <div class="col-6">
                {% for meta_data, flame_graph in zipped_benchmark_data %}
                    <object id="{{meta_data.sample_id}}" name="{{meta_data.sample_id}}">
                        <div class="d-flex justify-content-center">
                            {{flame_graph}}
                        </div>
                        <br>
                        <p class="d-flex justify-content-center"> Sample ID: {{meta_data.sample_id}}</p>
                    </object>
                {% endfor %}
            </div>
            <div class="col-6">
                {% for meta_data, flame_graph in zipped_baseline_data %}
                    <object id="{{meta_data.sample_id}}" name="{{meta_data.sample_id}}">
                        <div class="d-flex justify-content-center">
                            {{flame_graph}}
                        </div>
                        <br>
                        <p class="d-flex justify-content-center"> Sample ID: {{meta_data.sample_id}}</p>
                    </object>
                {% endfor %}
            </div>
        </div>
    </div>
</body>
</html>
"""
