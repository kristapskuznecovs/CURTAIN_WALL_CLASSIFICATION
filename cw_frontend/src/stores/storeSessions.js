import { makeObservable, observable, action } from 'mobx';
import { v4 as uuidv4 } from 'uuid';

class SessionStore {
    sessionId = localStorage.getItem('session_id') || null;

  constructor() {
    makeObservable(this, {
      sessionId: observable,
      setSessionId: action,
      generateSessionId: action,
    });
  }

  setSessionId(sessionId) {
    this.sessionId = sessionId;
    localStorage.setItem('session_id', sessionId);
    console.log(`Session ID updated: ${sessionId}`);
  }

  generateSessionId() {
    const storedSessionId = localStorage.getItem('session_id');
    const storedSessionDate = localStorage.getItem('session_date');
    const currentDate = new Date().toLocaleDateString();

    if (!storedSessionId || storedSessionDate !== currentDate) {
      const newSessionId = uuidv4();
      localStorage.setItem('session_id', newSessionId);
      localStorage.setItem('session_date', currentDate);
      this.setSessionId(newSessionId);
      console.log(`New session ID generated: ${newSessionId}`);
    } else {
      this.setSessionId(storedSessionId);
    }
  }
}

const sessionStore = new SessionStore();

export { sessionStore };