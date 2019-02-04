from replapi import replit


repl = replit.ReplIt('reagentx')
urls = repl.get_urls()
print(f'Found {len(urls)} repls!')
repl.download_all()
