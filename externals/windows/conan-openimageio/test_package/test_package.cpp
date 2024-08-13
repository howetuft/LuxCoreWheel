#include <OpenImageIO/imagecache.h>

int main()
{
    using namespace OpenImageIO_v2_1;

    ImageCache* cache = ImageCache::create();
    ImageCache::destroy(cache);
}