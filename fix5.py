f = open("backend/src/find_api/core/storage_minio.py", "r")
c = f.read()
f.close()

# Fix 1: presigned URL path prefix
old1 = "            signing_client = self._public_client or self.client\n            return signing_client.presigned_get_object(\n                self.bucket, object_name, expires=timedelta(seconds=expires)\n            )"
new1 = "            signing_client = self._public_client or self.client\n            base_url = signing_client.presigned_get_object(\n                self.bucket, object_name, expires=timedelta(seconds=expires)\n            )\n            if self._public_client and settings.MINIO_PUBLIC_ENDPOINT:\n                parsed = urlparse(settings.MINIO_PUBLIC_ENDPOINT.rstrip(\"/\"))\n                base_path = parsed.path.rstrip(\"/\")\n                if base_path:\n                    signed_parsed = urlparse(base_url)\n                    base_url = urlunparse((signed_parsed.scheme, signed_parsed.netloc, base_path + signed_parsed.path, signed_parsed.params, signed_parsed.query, signed_parsed.fragment))\n            return base_url"

# Fix 2: to_thread wraps
old2 = "            self.client.remove_object(self.bucket, object_name)"
new2 = "            await asyncio.to_thread(self.client.remove_object, self.bucket, object_name)"

old3 = "            self.client.stat_object(self.bucket, object_name)"
new3 = "            await asyncio.to_thread(self.client.stat_object, self.bucket, object_name)"

c = c.replace(old1, new1).replace(old2, new2).replace(old3, new3)
f = open("backend/src/find_api/core/storage_minio.py", "w")
f.write(c)
f.close()
print("to_thread count:", c.count("to_thread"))
