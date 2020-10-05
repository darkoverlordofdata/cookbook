function bind_links() {
    $("a.md-link").on("click", load_and_render)
}

function load_and_render(e) {
    var src = e.target.dataset.md
    toc.navigate(src.slice(0,-9), {trigger: true})
    return false
    //suppress any other actions from happening
}

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
                title = text.match(/# (.*)/)[1]
                document.title = title
                bind_links()
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
            if ((/m(ark)?d(own)?$/gi).test(href)) {
                return `<a class="md-link" data-md="${href}" href="#">${text}</a>`
                // an empty href is used while the markdown document is stored
                // in the data-md attribute
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
        bind_links()
        Backbone.history.start({pushstate: true})

    })
}
main()