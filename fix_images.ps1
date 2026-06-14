$file = "c:\Users\DELL\Desktop\Amoha\cardmilk.html"
$content = Get-Content $file -Raw

# Use Wikipedia/Wikimedia Commons URLs — these allow hotlinking
$imgs = @(
    @{ old = 'alt="Heritage Full Cream Milk"'; new = 'src="https://upload.wikimedia.org/wikipedia/en/thumb/b/b9/Heritage_Foods_logo.png/220px-Heritage_Foods_logo.png" onerror="this.src=''card1.png.jpeg''" alt="Heritage Full Cream Milk"' },
    @{ old = 'alt="Amul Taaza Milk"'; new = 'src="https://upload.wikimedia.org/wikipedia/en/thumb/b/b7/Amul_Taaza.jpg/220px-Amul_Taaza.jpg" onerror="this.src=''milk.png.jpeg''" alt="Amul Taaza Milk"' },
    @{ old = 'alt="Amul Cow Milk"'; new = 'src="https://upload.wikimedia.org/wikipedia/commons/thumb/b/b3/Amul_logo.svg/200px-Amul_logo.svg.png" onerror="this.src=''milk.jpeg''" alt="Amul Cow Milk"' },
    @{ old = 'alt="Nandini Toned Milk"'; new = 'src="https://upload.wikimedia.org/wikipedia/en/thumb/9/91/KMF_logo.png/200px-KMF_logo.png" onerror="this.src=''milk.jpeg''" alt="Nandini Toned Milk"' },
    @{ old = 'alt="Condensed Milk"'; new = 'src="https://upload.wikimedia.org/wikipedia/commons/thumb/6/6d/Good_Food_Display_-_NCI_Visuals_Online.jpg/220px-Good_Food_Display_-_NCI_Visuals_Online.jpg" onerror="this.src=''milkmaid.jpeg''" alt="Condensed Milk"' }
)

# Replace only the src part before each alt, keeping alt intact
foreach ($item in $imgs) {
    $pattern = 'src="[^"]*" (onerror="[^"]*" )?alt="' + [regex]::Escape(($item.old -replace '^alt="' -replace '"$' ))  + '"'
    $replacement = $item.new
    $content = [regex]::Replace($content, $pattern, $replacement)
}

Set-Content $file $content -NoNewline
Write-Host "Done"
