db.flickr_pics.find().forEach( function(u) { u.tumblr_blogurl = u.tumblr_blogurl.replace(/http\:\/\//g, "").replace(/\//, ""); db.flickr_pics.save(u); } );
