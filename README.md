# Unofficial repl.it API

I wanted to download all of my REPLs regularly and sync them to my GitHub; since there was no way to do that I made this package. This project uses the GraphQL data that powers repl.it to enumberate a list of repls and download them.

## Usage

    from replapi import replit
    repl = replit.ReplIt('username')
    repl.download_all()
