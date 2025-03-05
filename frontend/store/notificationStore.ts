/** Nuxt Store module: notificationStore module use to handle error message dispaly in snackbar
 *
 * err: Error message content as JSON Object: "err" variable is listened by watcher. Value change
 * triggers the display of message in snackbar (refer error-snackbar component)
 */

import { defineStore } from "pinia";
import type { NotificationInfo } from "~/types/notifications"

export const useNotificationStore = defineStore("notifications", {
  state: () => ({ info: null as NotificationInfo | null, }),
  actions: {
    setInfo(info: NotificationInfo ) {
      this.info = info;
    },
    resetInfo() {
      this.info=null
    }
  },
});
