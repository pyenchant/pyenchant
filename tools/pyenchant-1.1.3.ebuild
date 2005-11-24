# Written by Ryan Kelly, 2004
# This script is placed in the public domain

inherit distutils

DESCRIPTION="Python wrapper for the Enchant spellchecking wrapper library"
SRC_URI="mirror://sourceforge/pyenchant/${P}.tar.gz"
HOMEPAGE="http://pyenchant.sourceforge.net"

IUSE=""
SLOT="0"
KEYWORDS="~x86 ~amd64"
LICENSE="LGPL-2.1"

DEPEND=">=dev-lang/python-2.3
        >=app-text/enchant-1.1.6"


