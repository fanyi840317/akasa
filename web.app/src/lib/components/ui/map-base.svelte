export let categories: string[] = [];

$effect(() => {
  if (categories.length > 0) {
    // 根据分类过滤标记点
    const filteredMarkers = markers.filter(marker => 
      categories.includes(marker.category)
    );
    setMarkers(filteredMarkers);
  } else {
    setMarkers(markers);
  }
}); 