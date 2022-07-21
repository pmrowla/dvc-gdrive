import pytest
from dvc.fs import GDriveFileSystem

from .cloud import GDrive


@pytest.fixture
def make_gdrive(make_tmp_dir):
    def _make_gdrive():
        from urllib.parse import urlparse

        # NOTE: temporary workaround
        tmp_dir = make_tmp_dir("gdrive", dvc=True)

        url = GDrive.get_url()
        ret = GDrive(url)
        fs = GDriveFileSystem(
            gdrive_credentials_tmp_dir=tmp_dir.dvc.tmp_dir, **ret.config
        )

        parsed = urlparse(url)
        bucket = parsed.hostname
        path = parsed.path.lstrip("/")
        
        fs.fs._gdrive_create_dir(  # noqa, pylint: disable=protected-access
            bucket, path  # noqa, pylint: disable=protected-access
        )
        return ret

    return _make_gdrive


@pytest.fixture
def gdrive(make_gdrive):
    return make_gdrive()
