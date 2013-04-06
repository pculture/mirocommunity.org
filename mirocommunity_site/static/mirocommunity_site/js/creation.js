;jQuery(function($){
    function precacheBackgroundImage(classes){
        var obj = $("<div class='" + classes + "' style='display: none'></div>");
        // Need to append to body to get computed css in Chrome or Safari.
        obj.appendTo('body');
        // Either "none" or url("...urlhere..")
        var backgroundImage = obj.css('background-image'),
            imageURL = backgroundImage.match(/^url\(['"](.+)["']\)$/);
        // If matched, retrieve url, otherwise ""
        imageURL = imageURL ? imageURL[1] : "";
        if (imageURL != "") {
            var img = new Image();
            img.src = imageURL;
        }
        obj.remove();
    }
    precacheBackgroundImage('creation-ball');
    precacheBackgroundImage('creation-ball red');

    $('form').submit(function(e){
        var div = $('<div class="creation-overlay"></div>'),
            message = $("<div class='creation-message'><h1>Your site is being created</h1><h2>This may take a minute. Please don't close your browser.</h2></div>");
        for(var i=0; i<11; i++) {
            if (i % 2 == 0) {
                message.append($("<div class='creation-ball'></div>"));
            } else {
                message.append($("<div class='creation-ball red'></div>"));
            }
        }

        div.appendTo('body');
        div.append(message);
        div.height($(document).height());
        div.width($(document).width());
    });
});