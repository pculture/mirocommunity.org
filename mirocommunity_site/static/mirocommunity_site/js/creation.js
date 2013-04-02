;jQuery(function($){
    $("<div class='creation-ball'></div>");
    $("<div class='creation-ball red'></div>");
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