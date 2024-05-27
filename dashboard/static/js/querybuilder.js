// variables 
var colresults;
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


$("#clearText").on("click", function () {
    document.getElementById("rawquery").value = "";
});

$("#qry_layers").on("change", function () {
    if ($("#qry_layers").val() != "--SELECT LAYER--") {
        document.getElementById("qry_columns").innerHTML = "";
        fetch(

            "https://geonode.communitygis.in/geoserver/ows?service=WFS&version=1.0.0&request=describeFeatureType&typename=" +
            $("#qry_layers").val() +
            "&outputFormat=application%2Fjson"
        )
            .then((response) => response.json())
            .then((result) => {
                colresults = result
                var option = document.createElement("option");
                option.innerText = "--SELECT COLUMN--";
                option.selected = true;
                document.getElementById("qry_columns").appendChild(option);
                var properties = result.featureTypes[0].properties;
                for (var i = 0; i < properties.length; i++) {
                    if (properties[i].name === "geom") continue;
                    var option = document.createElement("option");
                    option.innerText = properties[i].name;
                    option.value = properties[i].name;
                    document.getElementById("qry_columns").appendChild(option);
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
        document.getElementById("rawquery").value = $("#qry_columns").val();
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
    if ($("#qry_layers").val() != "--SELECT VALUE--") {
        document.getElementById("rawquery").value += isNaN($("#qry_values").val())
            ? "'" + $("#qry_values").val() + "'"
            : $("#qry_values").val();
    }
});
$("#qry_operator").on("change", function () {
    if ($("#qry_layers").val() != "--SELECT VALUE--") {
        document.getElementById("rawquery").value += isNaN($("#qry_operator").val())
            ? "" + $("#qry_operator").val() + ""
            : $("#qry_operator").val();
    }
});


function showQueryResult() {
    var rawQuery = $("#rawquery").val();
    var operator = $("#qry_operator").val();
    if (operator.toLowerCase() === "like" && rawQuery.includes("LIKE")) {
        rawQuery = rawQuery.replace(/LIKE/gi, "");
        rawQuery = rawQuery.trim(); // Remove leading/trailing spaces if needed
        rawQuery = "%25" + rawQuery + "%25";


    }
    var url =
        "https://geonode.communitygis.in/geoserver/geonode/ows?service=WFS&version=1.0.0&request=GetFeature&typeName=" +
        $("#qry_layers").val() +
        "&outputFormat=application%2Fjson&CQL_FILTER=(" +
        $("#rawquery").val() +
        ")";

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
                addGeoJSONLayer(result);
            }
        })
}

