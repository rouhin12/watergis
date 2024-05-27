// variables 
var colresults;
var currentQuery = ""; 
function getDataType(columnName) {
    var featureType = colresults.featureTypes[0]; // Assuming you have the 'result' variable available from the API response
    var properties = featureType.properties;

    for (var i = 0; i < properties.length; i++) {
        if (properties[i].name === columnName) {
            return properties[i].type;
        }
    }

    return null;
}

function addOption(selectElement, value, text) {
    var option = document.createElement("option");
    option.value = value;
    option.innerText = text;
    selectElement.appendChild(option);
}

var layer
function addGeoJSONLayer(geoJSONData) {
    layer = L.geoJSON(geoJSONData, {
        style: function (feature) {
            // Define the style for each feature
            return {
                fillColor: 'yellow',
                fillOpacity: 0.5,
                color: 'black',
                weight: 2
            };
        },
        onEachFeature: function (feature, layer) {
            // Extract the properties object
            var properties = feature.properties;

            // Create a dynamic popup content string using all attributes of the layer
            var popupContent = "<div class='popup-content'>";
            for (var key in properties) {
                popupContent += "<b>" + key + ":</b> " + properties[key] + "<br>";
            }
            popupContent += "</div>";

            // Bind the popup to the layer
            layer.bindPopup(popupContent, {
                className: 'custom-popup'
            });
        }
    }).addTo(mymap);

    // Fly to the bounds of the layer
    mymap.flyToBounds(layer.getBounds());
}

function clearGraphic() {
    // Check if the GeoJSON layer exists
    if (layer) {
        // Remove the GeoJSON layer from the map
        mymap.removeLayer(layer);

        // Set the reference to null
        layer = null;
    }
}

$("#enableColumn2").on("change", function () {
    if ($(this).is(":checked")) {
        $("#column2Options").show();
    } else {
        $("#column2Options").hide();
    }
});

function clearAllOptions() {
    $("#qry_layers").val("--SELECT LAYER--").change();
    $("#qry_columns").val("").change();
    $("#qry_operator").val("").change();
    $("#qry_values").val("").change();
    $("#qry_columns_2").val("").change();
    $("#qry_operator_2").val("").change();
    $("#qry_values_2").val("").change();
    $("#qry_logical_operator").val("AND").change();
}

$("#clearText").on("click", function () {
    document.getElementById("rawquery").value = "";
    clearAllOptions();
    // $("#addAnotherLayerCheckbox").prop("checked", false);
});
das
// $("#addAnotherLayerCheckbox").on("change", function () {
//     if ($(this).is(":checked")) {
//         // Clear options selected for the previous layer
//         clearAllOptions();
//     }
// });

$("#qry_layers").on("change", function () {
    if ($("#qry_layers").val() != "--SELECT LAYER--") {
        document.getElementById("qry_columns").innerHTML = "";
        document.getElementById("qry_columns_2").innerHTML = "";
        console.log("Selected Layer:", $("#qry_layers").val());
        fetch(

            "https://geonode.communitygis.in/geoserver/ows?service=WFS&version=1.0.0&request=describeFeatureType&typename=" +
            $("#qry_layers").val() +
            "&outputFormat=application%2Fjson"
        )
            .then((response) => response.json())
            .then((result) => {
                colresults = result
                var option1 = document.createElement("option");
                option1.innerText = "--SELECT COLUMN 1--";
                option1.selected = true;
                document.getElementById("qry_columns").appendChild(option1);
                var option2 = document.createElement("option");
                option2.innerText = "--SELECT COLUMN 2--";
                option2.selected = true;
                document.getElementById("qry_columns_2").appendChild(option2);
                var properties = result.featureTypes[0].properties;
                for (var i = 0; i < properties.length; i++) {
                    if (properties[i].name === "geom") continue;
                    var option = document.createElement("option");
                    option.innerText = properties[i].name;
                    option.value = properties[i].name;
                    document.getElementById("qry_columns").appendChild(option);

                    var option_col2 = document.createElement("option");
                    option_col2.innerText = properties[i].name;
                    option_col2.value = properties[i].name;
                    document.getElementById("qry_columns_2").appendChild(option_col2);
                }
                // $("#qry_columns").select2("destroy").select2()
            })
            .catch((error) => console.log("error", error));
    }
});

$("#qry_columns").on("change", function () {
    if ($("#qry_columns").val() != "--SELECT COLUMN--") {
        var selectedColumn = $("#qry_columns").val();
        var operatorSelect = document.getElementById("qry_operator");
        operatorSelect.innerHTML = ""; // Clear previous options

        if (selectedColumn) {
            var dataType = getDataType(selectedColumn); // Get the data type based on the selected column

            if (dataType === "xsd:int" || dataType === "xsd:double" || dataType === "xsd:number") {
                addOption(operatorSelect, "", "Select Option");
                addOption(operatorSelect, ">", "Greater than");
                addOption(operatorSelect, "<", "Less than");
                addOption(operatorSelect, ">=", "Greater than or equal to");
                addOption(operatorSelect, "<=", "Less than or equal to");
                addOption(operatorSelect, "=", "Equal to");
            } else if (dataType === "xsd:string") {
                addOption(operatorSelect, "", "Select Option");
                addOption(operatorSelect, "=", "Equal to");
                addOption(operatorSelect, "+LIKE+", "Like");
            }
        }

        document.getElementById("qry_values").innerHTML = "";
        // document.getElementById("rawquery").value = $("#qry_columns").val();
        fetch(
            "https://geonode.communitygis.in/geoserver/ows?service=WFS&version=1.0.0&request=GetFeature&typename=" +
            $("#qry_layers").val() +
            "&PROPERTYNAME=" +
            $("#qry_columns").val() +
            "&outputFormat=application%2Fjson"
        )
            .then((response) => response.json())
            .then((result) => {
                var uniqval = [];
                var features = result.features;
                for (var i = 0; i < features.length; i++) {
                    if (
                        !uniqval.includes(features[i].properties[$("#qry_columns").val()])
                    )
                        uniqval.push(features[i].properties[$("#qry_columns").val()]);
                }
                var option = document.createElement("option");
                option.innerText = "--SELECT VALUE--";
                option.selected = true;
                document.getElementById("qry_values").appendChild(option);
                for (var i = 0; i < uniqval.length; i++) {
                    var option = document.createElement("option");
                    option.innerText = uniqval[i];
                    option.value = uniqval[i];
                    document.getElementById("qry_values").appendChild(option);
                }
                // $("#qry_values").select2("destroy").select2()
            })
            .catch((error) => console.log("error", error));
    }
});

$("#qry_values").on("change", function () {
    if ($("#qry_values").val() != "--SELECT VALUE--") {
        var currentQuery = document.getElementById("rawquery").value;
        var newValue = isNaN($("#qry_values").val()) ? "'" + $("#qry_values").val() + "'" : $("#qry_values").val();
        document.getElementById("rawquery").value = currentQuery + newValue;
    }
});
$("#qry_operator").on("change", function () {
    if ($("#qry_operator").val() != "--SELECT VALUE--") {
        var currentQuery = document.getElementById("rawquery").value;
        document.getElementById("rawquery").value = currentQuery + " " + $("#qry_operator").val() + " ";
    }
});

$("#qry_columns_2").on("change", function () {
    if ($("#qry_columns_2").val() != "--SELECT COLUMN 2--") {
        var selectedColumn = $("#qry_columns_2").val();
        var operatorSelect = document.getElementById("qry_operator_2");
        operatorSelect.innerHTML = ""; // Clear previous options

        if (selectedColumn) {
            var dataType = getDataType(selectedColumn); // Get the data type based on the selected column

            if (dataType === "xsd:int" || dataType === "xsd:double" || dataType === "xsd:number") {
                addOption(operatorSelect, "", "Select Option");
                addOption(operatorSelect, ">", "Greater than");
                addOption(operatorSelect, "<", "Less than");
                addOption(operatorSelect, ">=", "Greater than or equal to");
                addOption(operatorSelect, "<=", "Less than or equal to");
                addOption(operatorSelect, "=", "Equal to");
            } else if (dataType === "xsd:string") {
                addOption(operatorSelect, "", "Select Option");
                addOption(operatorSelect, "=", "Equal to");
                addOption(operatorSelect, "+LIKE+", "Like");
            }
        }

        document.getElementById("qry_values_2").innerHTML = "";
        // document.getElementById("rawquery").value = $("#qry_columns_2").val();
        fetch(
            "https://geonode.communitygis.in/geoserver/ows?service=WFS&version=1.0.0&request=GetFeature&typename=" +
            $("#qry_layers").val() +
            "&PROPERTYNAME=" +
            $("#qry_columns_2").val() +
            "&outputFormat=application%2Fjson"
        )
            .then((response) => response.json())
            .then((result) => {
                var uniqval = [];
                var features = result.features;
                for (var i = 0; i < features.length; i++) {
                    if (
                        !uniqval.includes(features[i].properties[$("#qry_columns_2").val()]))
                        uniqval.push(features[i].properties[$("#qry_columns_2").val()]);
                }
                var option = document.createElement("option");
                option.innerText = "--SELECT VALUE 2--";
                option.selected = true;
                document.getElementById("qry_values_2").appendChild(option);
                for (var i = 0; i < uniqval.length; i++) {
                    var option = document.createElement("option");
                    option.innerText = uniqval[i];
                    option.value = uniqval[i];
                    document.getElementById("qry_values_2").appendChild(option);
                }
                
            })
            .catch((error) => console.log("error", error));
    }
    
});

$("#qry_values_2").on("change", function () {
    if ($("#qry_values_2").val() != "--SELECT VALUE 2--") {
        var currentQuery = document.getElementById("rawquery").value;
        var newValue = isNaN($("#qry_values_2").val()) ? "'" + $("#qry_values_2").val() + "'" : $("#qry_values_2").val();
        var operator = $("#qry_operator_2").val();
        var queryPart = (operator.toLowerCase() === "like") ? 
                        $("#qry_columns_2").val() + " " + operator + " '%" + $("#qry_values_2").val() + "%'" :
                        $("#qry_columns_2").val() + " " + operator + " " + newValue;
        document.getElementById("rawquery").value = currentQuery ? currentQuery + " AND " + queryPart : queryPart;
    }
});

$("#qry_operator_2").on("change", function () {
    if ($("#qry_operator_2").val() != "--SELECT VALUE 2--") {
        var currentQuery = document.getElementById("rawquery").value;
        var operator = $("#qry_operator_2").val();
        document.getElementById("rawquery").value = currentQuery + " " + operator + " ";
    }
});

function showQueryResult() {
    var column1 = $("#qry_columns").val();
    var operator1 = $("#qry_operator").val();
    var value1 = $("#qry_values").val();
    var logicalOperator = $("#qry_logical_operator").val();
    var column2 = $("#qry_columns_2").val();
    var operator2 = $("#qry_operator_2").val();
    var value2 = $("#qry_values_2").val();

    var queryPart1 = "";
    var queryPart2 = "";

    // Construct the first part of the query
    if (column1 && operator1 && value1) {
        if (operator1.toLowerCase() === "like") {
            queryPart1 = column1 + " LIKE '%" + value1 + "%'";
        } else {
            queryPart1 = column1 + " " + operator1 + " " + (isNaN(value1) ? "'" + value1 + "'" : value1);
        }
    }

    // Construct the second part of the query
    if (column2 && operator2 && value2) {
        if (operator2.toLowerCase() === "like") {
            queryPart2 = column2 + " LIKE '%" + value2 + "%'";
        } else {
            queryPart2 = column2 + " " + operator2 + " " + (isNaN(value2) ? "'" + value2 + "'" : value2);
        }
    }

    // Combine the query parts with the logical operator
    var rawQuery = queryPart1;
    if (queryPart1 && queryPart2) {
        rawQuery += " " + logicalOperator + " " + queryPart2;
    } else if (queryPart2) {
        rawQuery = queryPart2;
    }

    console.log("Column 1:", column1);
    console.log("Operator 1:", operator1);
    console.log("Value 1:", value1);
    console.log("Query Part 1:", queryPart1);
    console.log("Logical Operator:", logicalOperator);
    console.log("Column 2:", column2);
    console.log("Operator 2:", operator2);
    console.log("Value 2:", value2);
    console.log("Query Part 2:", queryPart2);
    console.log("Combined Query:", rawQuery);

    $("#rawquery").val(rawQuery);

    if (!rawQuery) {
        swal({
            position: "center",
            icon: "error",
            title: "No query parts to combine!",
            showConfirmButton: false,
            timer: 2000,
        });
        return;
    }

    var url =
        "https://geonode.communitygis.in/geoserver/geonode/ows?service=WFS&version=1.0.0&request=GetFeature&typeName=" +
        $("#qry_layers").val() +
        "&CQL_FILTER=" + encodeURIComponent(rawQuery) + "&outputFormat=application%2Fjson";

    fetch(url)
        .then(res => res.json())
        .then(result => {
            if (result.features.length == 0) {
                swal({
                    position: "center",
                    icon: "error",
                    title: "No result found for the query!",
                    showConfirmButton: false,
                    timer: 2000,
                });
            } else {
                clearGraphic();
                addGeoJSONLayer(result);
            }
        })
        .catch(error => console.log("error", error));
}