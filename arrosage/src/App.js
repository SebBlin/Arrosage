import React from 'react';

import Scheduler, { Resource } from 'devextreme-react/scheduler';

import { data, resourcesData } from './data.js';
import * as AspNetData from 'devextreme-aspnet-data-nojquery';

// const url = 'https://js.devexpress.com/Demos/Mvc/api/SchedulerData';
const url = 'http://gw:5000';
const dataSource = AspNetData.createStore({
  key: 'AppointmentId',
  loadUrl: `${url }/Get`,
  insertUrl: `${url }/Post`,
  updateUrl: `${url }/Put`,
  deleteUrl: `${url }/Delete`,
  onBeforeSend(_, ajaxOptions) {
    ajaxOptions.xhrFields = { withCredentials: true };
  }
});

const currentDate = new Date(2020, 4, 9);
// const currentDate = new Date(2017, 4, 23);
const views = ['agenda','day', 'week', 'month'];

class App extends React.Component {
  render() {
    return (
      <Scheduler
        dataSource={dataSource}
        // dataSource={data}
        views={views}
        defaultCurrentView="week"
        defaultCurrentDate={currentDate}
        firstDayOfWeek={1}
        startDayHour={9}
        height={800}
        textExpr= "Text"
        // startDateExpr="StartDate"
        // endDateExpr="EndDate"
        allDayExpr="AllDay"
      >
        <Resource
          dataSource={resourcesData}
          fieldExpr="roomId"
          label="Room"
        />
      </Scheduler>
    );
  }
}

export default App;

