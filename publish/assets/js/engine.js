
function main() {
    //prep backbone
    var Router = Backbone.Router.extend({
        routes: {
            ":recipe": "recipe",
        },
        recipe: function(recipe) {
            var file = recipe+".markdown"
            $.get(file, function(text) {
                $("#content").html(marked(text))
                var title_re = /# (.*)/
                title = text.match(title_re)[1]
                document.title = title
            })
        }
    })

    toc = new Router()
    // toc stands for table of contents, not the best name but *shrugs*

    // prep marked
    var renderer = {
    // holds the tags we want to modify
        link: function(href, title, text) {
        // <a> tag
            var name = href.match(/(.*?)(\.markdown)/i)
            console.log(name)
            if (name != null) {
                return `<a class="md-link" href="#${name[1]}">${text}</a>`
            } else {
                return false
                // return false to fallback to default
            }
        }
    }

    marked.use({ // specify the options we want to use
        renderer: renderer,
        gfm: true, // Github Flavored Markdown, need for below
        breaks: true, // turn linebreaks into <br> so we don't need the two space hack
    })

    $(document).ready(function() {
        Backbone.history.start({pushstate: true})

    })
}
main()