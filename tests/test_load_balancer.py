import pytest
from unittest.mock import patch
from load_balancer.balancer import LoadBalancer

@pytest.fixture
def vps_list():
    return ['http://vps1.example.com', 'http://vps2.example.com', 'http://vps3.example.com']

def test_load_vps_list(vps_list, mocker):
    mock_load_from_file = mocker.patch('load_balancer.balancer.VPSManager.load_from_file')
    mock_health_checker_set_vps_list = mocker.patch('load_balancer.balancer.HealthChecker.set_vps_list')
    mock_metrics_setup = mocker.patch('load_balancer.balancer.Metrics.setup')
    mock_configuration_load = mocker.patch('load_balancer.balancer.Configuration.load')

    load_balancer = LoadBalancer()
    load_balancer.vps_manager.load_from_file.return_value = vps_list
    load_balancer.load_vps_list('vps_list.txt')

    mock_load_from_file.assert_called_once_with('vps_list.txt')
    mock_health_checker_set_vps_list.assert_called_once_with(vps_list)
    mock_metrics_setup.assert_called_once()
    mock_configuration_load.assert_called_once()

def test_add_vps(mocker):
    mock_vps_manager_add_vps = mocker.patch('load_balancer.balancer.VPSManager.add_vps')
    mock_health_checker_add_vps = mocker.patch('load_balancer.balancer.HealthChecker.add_vps')

    load_balancer = LoadBalancer()
    vps = 'http://vps1.example.com'
    load_balancer.add_vps(vps)

    mock_vps_manager_add_vps.assert_called_once_with(vps)
    mock_health_checker_add_vps.assert_called_once_with(vps)

def test_remove_vps(mocker):
    mock_vps_manager_remove_vps = mocker.patch('load_balancer.balancer.VPSManager.remove_vps')
    mock_health_checker_remove_vps = mocker.patch('load_balancer.balancer.HealthChecker.remove_vps')

    load_balancer = LoadBalancer()
    vps = 'http://vps1.example.com'
    load_balancer.remove_vps(vps)

    mock_vps_manager_remove_vps.assert_called_once_with(vps)
    mock_health_checker_remove_vps.assert_called_once_with(vps)


def test_get_next_vps_round_robin(vps_list, mocker):
    load_balancer = LoadBalancer(balancing_algorithm='round_robin')
    load_balancer.vps_list = vps_list


    mocker.patch.object(load_balancer.health_checker, 'check_health').return_value = True


    load_balancer.health_checker.check_health.side_effect = [True, True, True]

    assert load_balancer.get_next_vps() == 'http://vps1.example.com'
    assert load_balancer.get_next_vps() == 'http://vps2.example.com'
    assert load_balancer.get_next_vps() == 'http://vps3.example.com'
    assert load_balancer.get_next_vps() == 'http://vps1.example.com'