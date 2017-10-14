#!/usr/bin/env python
import unittest
import BTRFS

class TestStringMethods(unittest.TestCase):
    def setUp(self):
        
        self.btrfs = BTRFS.BTRFS()
        self.match_dirname_lines = [
                ['/dev/sdb3', '/root', '/'], 
                ['/dev/sdb1', '',      '/boot'], 
                ['/dev/sdc', '/archive', '/opt/archive'],
                ['/dev/sdc', '/home', '/home'],
                ['/dev/sdb3','/root/var/lib/docker/btrfs', '/var/lib/docker/btrfs'],
                ['/dev/sdf1', '',  '/var/lib/docker/a/b']
                ]

	self.subvolumes = [
                'ID 40507 gen 1401435 top level 258 path root/var/lib/docker/btrfs/subvolumes/74b994a949e5db9d507549832506b7e936cda600c6d649f1112a98dd137375cd', 
                'ID 40511 gen 1401439 top level 258 path root/var/lib/docker/btrfs/subvolumes/4c86f7421094a2108a94929e4106e35de31cb5ee6330d17c42b066bf1a184900',
                'ID 40512 gen 1401441 top level 258 path root/var/lib/docker/btrfs/subvolumes/afaea5dd79a11c5f8228b3d836c19a8c75d9ad301ba4d2786dae2420e21596da'
                ]
        self.subvolumes2 = [
                'ID 263 gen 38 top level 5 path var/lib/docker/btrfs/subvolumes/c53785138f44a3ffe08e4de3d1f59ef0e56dac78ff652aa68cf12c6d3080dbef',
                'ID 264 gen 42 top level 5 path var/lib/docker/btrfs/subvolumes/7810c3e9055c7369878733108bdd009789a15e862aae281311ff7a807fa55176',
                'ID 265 gen 45 top level 5 path var/lib/docker/btrfs/subvolumes/b1ea884335f5845dc5fc0c1fec5fb4cc3b15c1fc1d65d472472fa09477195599',
                'ID 266 gen 47 top level 5 path var/lib/docker/btrfs/subvolumes/55129ebf9cd4524bf3b5d5aefa0438747a1f5ccbaec3e2c9dac686b5f958e54f',
                'ID 267 gen 49 top level 5 path var/lib/docker/btrfs/subvolumes/6c89e63dd91a568b3c22d56d251e99c93acb5114ad64f0d2e7aec7f3175b443b', 
                'ID 268 gen 51 top level 5 path var/lib/docker/btrfs/subvolumes/a2ad25e9e023b09a7b291318d731c79db1a602d009db654ff9632ce6c78e7cb8',
                'ID 269 gen 53 top level 5 path var/lib/docker/btrfs/subvolumes/6ebf0955038684ac0f1ec1fe9ba3e4acc12e394a55b761d9b5b4efda29e3b4bd',
                'ID 270 gen 55 top level 5 path var/lib/docker/btrfs/subvolumes/11544846eb4ba21ac8a59bcae3a837d0da09a92cd241a4ca304d291ab6cf8dce',
                'ID 271 gen 57 top level 5 path var/lib/docker/btrfs/subvolumes/52568746f938d2746e07bf3a4e63559f0310ca8320a687bc2f8360540d641d76',
                'ID 272 gen 59 top level 5 path var/lib/docker/btrfs/subvolumes/800425d12149b307112525abd27d5bd4c8bce8bd45dfa40aca9cad21e8cb4489',
                'ID 273 gen 61 top level 5 path var/lib/docker/btrfs/subvolumes/aef2795b0d37b6b504ce1ba843b64578c182a487d49f30c76c25df981e35fd8e',
                'ID 274 gen 63 top level 5 path var/lib/docker/btrfs/subvolumes/c8da4f8a5222f26e4a855c7331e80db86d5907719f9d31f7a5fdac3e3c8259a6',
                'ID 275 gen 64 top level 5 path var/lib/docker/btrfs/subvolumes/45336f365c88e5bc750085abf551ca91ecf48690dab1c02df306cbefa390e311'
                ]

    def tearDown(self):
        self.btrfs = None

    def test_match_dirname_1(self):
	dirname='/var/lib/docker'
	lines = self.match_dirname_lines 

        self.assertEqual(self.btrfs.match_dirname(dirname,lines), ['/dev/sdb3', '/root', '/'])

    def test_match_dirname_2(self):
	dirname='/var/lib/docker/btrfs'
	lines = self.match_dirname_lines 
        self.assertEqual(self.btrfs.match_dirname(dirname,lines), [ '/dev/sdb3', '/root/var/lib/docker/btrfs', '/var/lib/docker/btrfs'])

    def test_match_dirname_3(self):
	dirname='/var/lib/docker/a'
	lines = self.match_dirname_lines 
        self.assertEqual(self.btrfs.match_dirname(dirname,lines), ['/dev/sdb3', '/root', '/'])

    def test_match_dirname_4(self):
	dirname =   '/var/lib/docker/btrfs/a/b/c'
	lines   =   self.match_dirname_lines
        self.assertEqual(self.btrfs.match_dirname(dirname,lines), ['/dev/sdb3', '/root/var/lib/docker/btrfs',  '/var/lib/docker/btrfs'] )

    def test_match_dirname_5(self):
	dirname =   '/var'
	lines   =   self.match_dirname_lines
        self.assertEqual(self.btrfs.match_dirname(dirname,lines), ['/dev/sdb3', '/root',  '/'] )

    def test_parse_btrfs_mount_1(self):
        source = "/"
        self.assertEqual(self.btrfs.parse_btrfs_mount(source), [ source, '' ])

    def test_parse_btrfs_mount_2(self):
        source = "/dev/sdb3[/root/var/lib/docker/btrfs]"
        self.assertEqual(self.btrfs.parse_btrfs_mount(source), [ '/dev/sdb3', '/root/var/lib/docker/btrfs' ] )

    def test_parse_btrfs_mount_3(self):
        source = "/dev/sdb3[/root/var/lib/docker/btrfs"
        self.assertEqual(self.btrfs.parse_btrfs_mount(source), [ source, '' ] )


    def test_subvolume_list_filter_1(self):
        subvolumes  = self.subvolumes
        btrfs_dir   = '/'
        btrfs_name  = 'root'
        targetdir   = '/var/lib/docker'
        source2     = ''
        result  = [ 
                '/var/lib/docker/btrfs/subvolumes/74b994a949e5db9d507549832506b7e936cda600c6d649f1112a98dd137375cd',
                '/var/lib/docker/btrfs/subvolumes/4c86f7421094a2108a94929e4106e35de31cb5ee6330d17c42b066bf1a184900',
                '/var/lib/docker/btrfs/subvolumes/afaea5dd79a11c5f8228b3d836c19a8c75d9ad301ba4d2786dae2420e21596da'
                ]
        self.assertEqual(self.btrfs.subvolume_list_filter(targetdir, btrfs_dir,btrfs_name, source2, subvolumes), result )

    def test_subvolume_list_filter_2(self):
        subvolumes  = self.subvolumes2
        btrfs_dir   = ''
        btrfs_name  = '<FS_TREE>'
        targetdir   = '/var/lib/docker'
        source2     = '/var/lib/docker'
        result  = [ 
                '/var/lib/docker/btrfs/subvolumes/c53785138f44a3ffe08e4de3d1f59ef0e56dac78ff652aa68cf12c6d3080dbef',
                '/var/lib/docker/btrfs/subvolumes/7810c3e9055c7369878733108bdd009789a15e862aae281311ff7a807fa55176',
                '/var/lib/docker/btrfs/subvolumes/b1ea884335f5845dc5fc0c1fec5fb4cc3b15c1fc1d65d472472fa09477195599',
                '/var/lib/docker/btrfs/subvolumes/55129ebf9cd4524bf3b5d5aefa0438747a1f5ccbaec3e2c9dac686b5f958e54f',
                '/var/lib/docker/btrfs/subvolumes/6c89e63dd91a568b3c22d56d251e99c93acb5114ad64f0d2e7aec7f3175b443b',
                '/var/lib/docker/btrfs/subvolumes/a2ad25e9e023b09a7b291318d731c79db1a602d009db654ff9632ce6c78e7cb8',
                '/var/lib/docker/btrfs/subvolumes/6ebf0955038684ac0f1ec1fe9ba3e4acc12e394a55b761d9b5b4efda29e3b4bd',
                '/var/lib/docker/btrfs/subvolumes/11544846eb4ba21ac8a59bcae3a837d0da09a92cd241a4ca304d291ab6cf8dce',
                '/var/lib/docker/btrfs/subvolumes/52568746f938d2746e07bf3a4e63559f0310ca8320a687bc2f8360540d641d76',
                '/var/lib/docker/btrfs/subvolumes/800425d12149b307112525abd27d5bd4c8bce8bd45dfa40aca9cad21e8cb4489',
                '/var/lib/docker/btrfs/subvolumes/aef2795b0d37b6b504ce1ba843b64578c182a487d49f30c76c25df981e35fd8e',
                '/var/lib/docker/btrfs/subvolumes/c8da4f8a5222f26e4a855c7331e80db86d5907719f9d31f7a5fdac3e3c8259a6',
                '/var/lib/docker/btrfs/subvolumes/45336f365c88e5bc750085abf551ca91ecf48690dab1c02df306cbefa390e311'
                ]
        self.assertEqual(self.btrfs.subvolume_list_filter(targetdir, btrfs_dir,btrfs_name, source2, subvolumes), result )




if __name__ == '__main__':
    #unittest.main()
    suite = unittest.TestLoader().loadTestsFromTestCase(TestStringMethods)
    unittest.TextTestRunner(verbosity=2).run(suite)
