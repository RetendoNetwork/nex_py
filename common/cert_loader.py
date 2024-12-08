from anynet import tls
import importlib.resources as resources


class CertificateLoader:
    def __init__(self, package_name):
        self.package_name = package_name

    def _get_file_path(self, file_name):
        resource_path = resources.files(self.package_name).joinpath(file_name)
        return resource_path

    def _read_file_content(self, file_name, mode="r", encoding="utf-8"):
        with self._get_file_path(file_name).open(mode, encoding=encoding) as file:
            return file.read()

    def _read_bytes_from_file(self, file_name):
        return self._get_file_path(file_name).read_bytes()

    def load_certificate(self, filename):
        raw_data = self._read_bytes_from_file(f"files/cert/{filename}")
        return tls.TLSCertificate.parse(raw_data, tls.TYPE_DER)

    def load_private_key(self, filename):
        raw_data = self._read_bytes_from_file(f"files/cert/{filename}")
        return tls.TLSPrivateKey.parse(raw_data, tls.TYPE_DER)