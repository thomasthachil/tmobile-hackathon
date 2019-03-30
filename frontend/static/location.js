var map, pin, datasource;
var animationTime = 5000;
var animation;
//Create an array of points to define a path to animate along.

var API_KEY = "LOmqa9yyQ5DuP12jbOaWzMGqqU9ok3eR-btZSrlGU5Q";

function GetMap() {
    //Initialize a map instance.
    map = new atlas.Map("results", {
        center: [-84.389, 33.777],
        zoom: 13,
        //Add your Azure Maps subscription key to the map SDK. Get an Azure Maps key at https://azure.com/maps
        authOptions: {
            authType: "subscriptionKey",
            subscriptionKey: API_KEY
        }
    });

    map.events.add("load", function() {
        //Create a data source and add it to the map.
        datasource = new atlas.source.DataSource();
        map.sources.add(datasource);

        //Add a layer for rendering the route lines and have it render under the map labels.
        map.layers.add(
            new atlas.layer.LineLayer(datasource, null, {
                strokeColor: "#2272B9",
                strokeWidth: 5,
                lineJoin: "round",
                lineCap: "round",
                filter: ["==", "$type", "LineString"]
            }),
            "labels"
        );

        //Add a layer for rendering point data.
        map.layers.add(
            new atlas.layer.SymbolLayer(datasource, null, {
                iconOptions: {
                    image: ["get", "icon"],
                    allowOverlap: true
                },
                textOptions: {
                    textField: ["get", "title"],
                    offset: [0, 1.2]
                },
                filter: ["==", "$type", "Point"]
            })
        );

        //Create the GeoJSON objects which represent the start and end points of the route.
        var startPoint = new atlas.data.Feature(
            new atlas.data.Point([-84.38, 33.757]),
            {
                title: "Customer",
                icon: "pin-blue"
            }
        );

        var endPoint = new atlas.data.Feature(
            new atlas.data.Point([-84.389, 33.777]),
            {
                title: "T-Mobile Tech Square",
                icon: "pin-round-blue"
            }
        );

        //Add the data to the data source.
        datasource.add([startPoint, endPoint]);

        map.setCamera({
            bounds: atlas.data.BoundingBox.fromData([startPoint, endPoint]),
            padding: 80
        });

        // Use SubscriptionKeyCredential with a subscription key
        var subscriptionKeyCredential = new atlas.service.SubscriptionKeyCredential(
            atlas.getSubscriptionKey()
        );

        // Use subscriptionKeyCredential to create a pipeline
        var pipeline = atlas.service.MapsURL.newPipeline(
            subscriptionKeyCredential
        );

        // Construct the RouteURL object
        var routeURL = new atlas.service.RouteURL(pipeline);

        //Start and end point input to the routeURL
        var coordinates = [
            [
                startPoint.geometry.coordinates[0],
                startPoint.geometry.coordinates[1]
            ],
            [endPoint.geometry.coordinates[0], endPoint.geometry.coordinates[1]]
        ];

        //Make a search route request
        routeURL
            .calculateRouteDirections(
                atlas.service.Aborter.timeout(10000),
                coordinates
            )
            .then(directions => {
                //Get data features from response
                var data = directions.geojson.getFeatures();
                datasource.add(data);
                // console.log(data)
                var tripTime =
                    data.features["0"].properties.legSummaries["0"]
                        .travelTimeInSeconds;
                tripTime = Math.round((tripTime / 60) * 100) / 100;
                document.getElementById("resultsText").innerHTML =
                    "<h5> Looks like they're " +
                    tripTime.toString() +
                    " minutes away! </h5>";

                var timeTillMeeting = document.getElementById("time").value;
                timeTillMeeting = Math.round(timeTillMeeting * 100) / 100;
                if (timeTillMeeting < tripTime) {
                    document.getElementById("resultsText").innerHTML +=
                        "<p> They'll be late by at least " +
                        Math.round(tripTime - timeTillMeeting).toString() +
                        " minutes. <br> Spread the love to our other customers while you wait. </p>";
                }
            });
    });
}
