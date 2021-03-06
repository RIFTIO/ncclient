from ncclient.operations.retrieve import *
import unittest
from mock import patch
from ncclient import manager
import ncclient.manager
import ncclient.transport
from ncclient.xml_ import *
from ncclient.operations import RaiseMode
from xml.etree import ElementTree
import copy


class TestRetrieve(unittest.TestCase):

    def setUp(self):
        self.device_handler = manager.make_device_handler({'name': 'junos'})

    @patch('ncclient.operations.retrieve.RPC._request')
    def test_get(self, mock_request):
        session = ncclient.transport.SSHSession(self.device_handler)
        obj = Get(session, self.device_handler, raise_mode=RaiseMode.ALL)
        root_filter = new_ele('filter')
        config_filter = sub_ele(root_filter, 'configuration')
        system_filter = sub_ele(config_filter, 'system')
        sub_ele(system_filter, 'services')
        obj.request(copy.deepcopy(root_filter))
        node = new_ele("get")
        node.append(util.build_filter(root_filter))
        xml = ElementTree.tostring(node, method='xml')
        call = mock_request.call_args_list[0][0][0]
        call = ElementTree.tostring(call, method='xml')
        self.assertEqual(call, xml)

    @patch('ncclient.operations.retrieve.RPC._request')
    def test_get_config(self, mock_request):
        session = ncclient.transport.SSHSession(self.device_handler)
        obj = GetConfig(session, self.device_handler, raise_mode=RaiseMode.ALL)
        source = "candidate"
        obj.request(source)
        node = new_ele("get-config")
        node.append(util.datastore_or_url("source", source))
        xml = ElementTree.tostring(node, method='xml')
        call = mock_request.call_args_list[0][0][0]
        call = ElementTree.tostring(call, method='xml')
        self.assertEqual(call, xml)

    @patch('ncclient.operations.retrieve.RPC._request')
    def test_dispatch(self, mock_request):
        session = ncclient.transport.SSHSession(self.device_handler)
        obj = Dispatch(session, self.device_handler, raise_mode=RaiseMode.ALL)
        rpc = 'get-software-information'
        source = "candidate"
        root_filter = new_ele('filter')
        config_filter = sub_ele(root_filter, 'configuration')
        system_filter = sub_ele(config_filter, 'system')
        sub_ele(system_filter, 'services')
        a = copy.deepcopy(root_filter)
        obj.request(rpc, source=source, filter=a)
        node = new_ele(rpc)
        node.append(util.datastore_or_url("source", source))
        node.append(util.build_filter(root_filter))
        xml = ElementTree.tostring(node, method='xml')
        call = mock_request.call_args_list[0][0][0]
        call = ElementTree.tostring(call, method='xml')
        self.assertEqual(call, xml)

    @patch('ncclient.operations.retrieve.RPC._request')
    def test_dispatch_2(self, mock_request):
        session = ncclient.transport.SSHSession(self.device_handler)
        obj = Dispatch(session, self.device_handler, raise_mode=RaiseMode.ALL)
        node = new_ele('get-software-information')
        source = "candidate"
        root_filter = new_ele('filter')
        config_filter = sub_ele(root_filter, 'configuration')
        system_filter = sub_ele(config_filter, 'system')
        sub_ele(system_filter, 'services')
        a = copy.deepcopy(root_filter)
        obj.request(node, source=source, filter=a)
        node.append(util.datastore_or_url("source", source))
        node.append(util.build_filter(root_filter))
        xml = ElementTree.tostring(node, method='xml')
        call = mock_request.call_args_list[0][0][0]
        call = ElementTree.tostring(call, method='xml')
        self.assertEqual(call, xml)
