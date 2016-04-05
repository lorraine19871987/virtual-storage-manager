$(function() {
    //check the status
    CheckTheStatus();

    //Update the table status
    setInterval(function(){
        UpdateBenchmarkStatus();
    }, 5000);
});

function CheckTheStatus(){
    $("td.status").each(function(){
        if(this.innerHTML == "running"){
            var html = "";
            html +="<div class='loading_gif'>";
            html +="    <img src=\"/static/dashboard/img/loading.gif\">";
            html +="</div>";
            html +=this.innerHTML;
            this.innerHTML = html;
        }
    });
}

function UpdateBenchmarkStatus(){
    $.ajax({
        data: "",
        type: "get",
        dataType: "json",
        url: "/dashboard/vsm/benchmark_case/update_benchmark_list/",
        success: function (cases) {
            var html = "";
            if(cases.length == 0){
                html += "<tr class=\"odd empty\">";
                html += "<td colspan=\"10\">No items to display.</td>";
                html += "</tr>";
            }
            else{
                for(var i=0;i<cases.length;i++){
                    html +="<tr id='benchmark_case_list__row__"+ i +" data-display='"+cases[i].name+"' data-object-id='"+cases[i].id+"' >";
                    html +="<td class=\"multi_select_column\">";
                    html +="<input class=\"table-row-multi-select\" name=\"object_ids\" value='"+cases[i].id+"' type=\"checkbox\"></input>";
                    html +="</td>";
                    html +="<td class=\"sortable normal_column\">"+cases[i].id+"</td>";
                    html +="<td class=\"sortable normal_column\">"+cases[i].name+"</td>";
                    html +="<td class=\"sortable normal_column\">"+cases[i].ioengine+"</td>";
                    html +="<td class=\"sortable normal_column\">"+cases[i].readwrite+"</td>";
                    var running_hosts = cases[i].running_hosts;
                    if(running_hosts == null || running_hosts == "") {
                        running_hosts = "-"
                    }
                    html +="<td class=\"sortable normal_column\">"+running_hosts+"</td>";
                    if(cases[i].status != "running"){
                        html +="<td class=\"sortable normal_column\">"+cases[i].status+"</td>";
                    }
                    else
                    {
                        html +="<td class=\"sortable normal_column\">";
                        html +="    <div class='loading_gif'>";
                        html +="        <img src=\"/static/dashboard/img/loading.gif\">";
                        html +="    </div>";
                        html +=cases[i].status;
                        html +="</td>";
                    }
                    html +="</tr>";
                }
            }
            $("#benchmark_case_list>tbody")[0].innerHTML = html;
        },
        error: function (XMLHttpRequest, textStatus, errorThrown) {
            if(XMLHttpRequest.status == 401)
                window.location.href = "/dashboard/auth/logout/";
        },
        complete: function(){

        }
    });
}