$file = "c:\Users\DELL\Desktop\Amoha\cardmilk.html"
$content = Get-Content $file -Raw

$urls = @(
    "https://images.unsplash.com/photo-1563636619-e9143da7973b?w=200&h=150&fit=crop",
    "https://images.unsplash.com/photo-1550583724-b2692b85b150?w=200&h=150&fit=crop",
    "https://images.unsplash.com/photo-1585435557343-3b092031a831?w=200&h=150&fit=crop",
    "https://images.unsplash.com/photo-1517448931760-9bf4414148b8?w=200&h=150&fit=crop",
    "https://images.unsplash.com/photo-1594937301426-5e00bab71fb3?w=200&h=150&fit=crop",
    "https://images.unsplash.com/photo-1600788886242-5c96aabe3757?w=200&h=150&fit=crop",
    "https://images.unsplash.com/photo-1628088062854-d1870b4553da?w=200&h=150&fit=crop",
    "https://images.unsplash.com/photo-1587657550754-5be90fcdad71?w=200&h=150&fit=crop",
    "https://images.unsplash.com/photo-1576186726115-4d51596775d1?w=200&h=150&fit=crop",
    "https://images.unsplash.com/photo-1523473827533-2a64d0d36748?w=200&h=150&fit=crop",
    "https://images.unsplash.com/photo-1571167530149-c1105da4c2c6?w=200&h=150&fit=crop",
    "https://images.unsplash.com/photo-1504674900247-0877df9cc836?w=200&h=150&fit=crop",
    "https://images.unsplash.com/photo-1464306076886-f8b74fa5b2b5?w=200&h=150&fit=crop",
    "https://images.unsplash.com/photo-1569050467447-ce54b3bbc37d?w=200&h=150&fit=crop",
    "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=200&h=150&fit=crop",
    "https://images.unsplash.com/photo-1544025162-d76694265947?w=200&h=150&fit=crop",
    "https://images.unsplash.com/photo-1496116218417-1a781b1c416c?w=200&h=150&fit=crop",
    "https://images.unsplash.com/photo-1559181567-c3190ca9be46?w=200&h=150&fit=crop",
    "https://images.unsplash.com/photo-1582515073490-39981397c445?w=200&h=150&fit=crop",
    "https://images.unsplash.com/photo-1565958011703-44f9829ba187?w=200&h=150&fit=crop",
    "https://images.unsplash.com/photo-1528750997573-59b89d56f4f7?w=200&h=150&fit=crop",
    "https://images.unsplash.com/photo-1606851094584-5f56b09b4f5c?w=200&h=150&fit=crop",
    "https://images.unsplash.com/photo-1540189549336-e6e99c3679fe?w=200&h=150&fit=crop",
    "https://images.unsplash.com/photo-1490474418585-ba9bad8fd0ea?w=200&h=150&fit=crop"
)

$i = 0
$fixed = [regex]::Replace($content, 'src="https://images\.unsplash\.com/[^"]*"', {
    param($m)
    $url = $urls[$i % $urls.Count]
    $script:i++
    return 'src="' + $url + '"'
})

Set-Content $file $fixed -NoNewline
Write-Host "Fixed $i image URLs"
