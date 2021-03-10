﻿Enum DnsQueryType {
    A = 1
    NS = 2
    MD = 3
    MF = 4
    CNAME = 5
    SOA = 6
    MB = 7
    MG = 8
    MR = 9
    NULL = 10
    WKS = 11
    PTR = 12
    HINFO = 13
    MINFO = 14
    MX = 15
    TXT = 16
    RP = 17
    AFSDB = 18
    X25 = 19
    ISDN = 20
    RT = 21
    NSAP = 22
    NSAPPTR = 23
    SIG = 24
    KEY = 25
    PX = 26
    GPOS = 27
    AAAA = 28
    LOC = 29
    NXT = 30
    EID = 31
    NIMLOC = 32
    SRV = 33
    ATMA = 34
    NAPTR = 35
    KX = 36
    CERT = 37
    A6 = 38
    DNAME = 39
    SINK = 40
    OPT = 41
    APL = 42
    DS = 43
    SSHFP = 44
    IPSECKEY = 45
    RRSIG = 46
    NSEC = 47
    DNSKEY = 48
    DHCID = 49
    NSEC3 = 50
    NSEC3PARAM = 51
    TLSA = 52
    SMIMEA = 53
    Unassigned = 54
    HIP = 55
    NINFO = 56
    RKEY = 57
    TALINK = 58
    CDS = 59
    CDNSKEY = 60
    OPENPGPKEY = 61
    CSYNC = 62
    SPF = 99
    UINFO = 100
    UID = 101
    GID = 102
    UNSPEC = 103
    NID = 104
    L32 = 105
    L64 = 106
    LP = 107
    EUI48 = 108
    EUI64 = 109
    TKEY = 249
    TSIG = 250
    IXFR = 251
    AXFR = 252
    MAILB = 253
    MAILA = 254
    All = 255
    URI = 256
    CAA = 257
    AVC = 258
    DOA = 259
    TA = 32768
    DLV = 32769
}
function Resolve-1111 {
    [CmdletBinding()]
    param (
        [Parameter(
            Mandatory,
            ValueFromPipeline,
            ValueFromPipelineByPropertyName,
            Position = 0
        )]
        [string[]]
        $HostName,

        [Parameter(
            ValueFromPipelineByPropertyName,
            Position = 1
        )]
        [DnsQueryType]
        $Type = 'A',

        [Parameter(DontShow)]
        [string]
        $ApiBaseUri = (Get-ApiBaseUri)
    )

    begin {
        $CtMimeType = Get-CtMimeType
    }

    process {
        foreach ($Lookup in $HostName) {
            Write-Verbose "Processing Name: $Lookup Type: $Type"
            $Uri = '{0}?ct={1}&name={2}&type={3}' -f @(
                $ApiBaseUri
                $CtMimeType
                $Lookup
                Resolve-QueryType $Type
            )
            Write-Verbose "Uri: $Uri"
            $Result = Invoke-RestMethod $Uri
            if ($Result -is [String]) {
                $Result -replace '""([^"]*)""', '"\"$1\""' | ConvertFrom-Json
            } else {
                $Result
            }
        }
    }
}
function Get-ApiBaseUri {
    [CmdletBinding()]
    param ()
    end {
        $Config = Import-Configuration
        $Config.CloudflareDnsApiBaseUri
    }
}
function Get-CtMimeType {
    [CmdletBinding()]
    param ()
    end {
        $Config = Import-Configuration
        $Config.CtMimeType
    }
}
function Resolve-QueryType {
    [CmdletBinding()]
    param (
        [Parameter(
            Mandatory,
            ValueFromPipeline,
            Position = 0
        )]
        [DnsQueryType[]]
        $QueryType
    )
    process {
        foreach ($type in $QueryType) {
            switch ($type) {
                'All' { '*' }
                'NSAPPTR' { 'NSAP-PTR' }
                Default { "$type"}
            }
        }
    }
}
if ('Core' -ne $PSVersionTable.PSEdition) {
    Enable-Tls -Tls12
}