#!/usr/bin/env coffee
#
# dependancies:
#   pandoc
#   xpdf 
#

fs = require('fs')
path = require('path')
{ exec, execSync } = require('child_process')


fix_extra_lines = (file) ->
    content = fs.readFileSync(file, 'utf8')
    while content.indexOf("\\\n") > 0
        content = content.replace("\\\n", "")
    fs.writeFileSync(file, content)
    return


# {.underline}
fix_underline = (file) ->
    content = fs.readFileSync(file, 'utf8')
    while content.indexOf("{.underline}") > 0
        content = content.replace("{.underline}", "()")
    fs.writeFileSync(file, content)
    return

fix_markdown = (file) ->
    content = fs.readFileSync(file, 'utf8')
    
    result = """
        ---
        title: #{path.basename(file, path.extname(file))}
        ref: #{path.basename(file, path.extname(file))}
        image: false
        time: 0
        category: food
        tags: {}
        ingredients: {}
        ---
        #{content}
        """
        
    fs.writeFileSync(file, result)
    return

console.log "hello world"
#
#
#   convert source docs from data/ to markdown in the _recipes/ folder.
#   Then update each markdown with a jekyl header parsed data from it's own content.
#


#
#   iterate over data/docx and data/odt
#
count = 0

fs.readdir "data/", (err, files) ->
    if err
        console.log err
        process.exit(1)
    files.forEach (file, index) ->
        switch path.extname(file)
            when '.docx'
                out = file.replace(".docx", ".markdown")
                cmd = "pandoc -o \"_recipes/#{out}\" \"data/#{file}\""
                exec cmd , (err, stdout, stderr) ->
                    if err
                        console.log err
                        process.exit(1)

                    fix_markdown "_recipes/#{out}"
                    
            when '.odt'
                cmd = "soffice --headless --convert-to htm --outdir ./data \"data/#{file}\" "
                execSync cmd
                src = file.replace(".odt", ".htm")
                out = file.replace(".odt", ".markdown")
                cmd = "pandoc -o \"_recipes/#{out}\" \"data/#{src}\""
                exec cmd , (err, stdout, stderr) ->
                    if err
                        console.log err
                        process.exit(1)

                    fix_markdown "_recipes/#{out}"
                    fix_extra_lines "_recipes/#{out}"
                    fix_underline "_recipes/#{out}"
            
            when '.pdf'
                out = file.replace(".pdf", "")
                cmd = "pdftohtml -s -i \"data/#{file}\" \"data/#{out}\""
                exec cmd , (err, stdout, stderr) ->
                    if err
                        console.log err
                        process.exit(1)

                    src = file.replace(".pdf", "-html.html")
                    out = file.replace(".pdf", ".markdown")
                    cmd = "pandoc -o \"_recipes/#{out}\" \"data/#{src}\""
                    exec cmd , (err, stdout, stderr) ->
                        if err
                            console.log err
                            process.exit(1)

                        fix_markdown "_recipes/#{out}"


                        
                    