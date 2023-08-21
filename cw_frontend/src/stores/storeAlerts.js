import { makeAutoObservable } from 'mobx';

class AlertStore {
  alerts = [];

  constructor() {
    makeAutoObservable(this);
  }

  showAlert(type, message) {
    this.alerts.push({ type, message });
  }

  hideAlert(alert) {
    this.alerts = this.alerts.filter((a) => a !== alert);
  }
}

export const alertStore = new AlertStore();