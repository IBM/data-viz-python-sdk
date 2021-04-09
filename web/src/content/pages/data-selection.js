import React, { useState, useEffect, useContext, useMemo } from 'react';
import { keys, has, isUndefined, includes, get, map, isEqual, pick, isEmpty } from 'lodash';

import {
  DataTableSkeleton,
  Dropdown,
  InlineNotification,
  Tooltip
} from 'carbon-components-react';

import { EnhancedDataTable } from '@console/pal/Components';

import EmptyWidget from '../wrappers/empty-widget';

import { DATA_TYPES } from '../../constants';

import DataContext from './context-data';

const DataSelection = () => {
  const {
    file,
    setDisableNext,
    selectedColumns, setSelectedColumns,
    selectedRows, setSelectedRows,
    selectedData, setSelectedData
  } = useContext(DataContext),
    [columns, setColumns] = useState(),
    [isLoading, setLoading] = useState(true),
    [error, setError] = useState(),
    COMPONENT_NAME = 'pages-data-selection';

  useEffect(() => {
    const reader = new FileReader();
    reader.onload = e => {
      const result = get(e, 'target.result', '')
      const data = get(result.match(/[^\r\n]+/g), [0], []).split(',');
      setColumns(data);
    };
    reader.onerror = e => setError(get(e, 'target.error'));
    reader.readAsText(file, 'UTF-8');
  }, [file]);

  useEffect(() => {
    setDisableNext(error || isEmpty(selectedRows) || !isEqual(
      selectedRows.length,
      keys(selectedColumns).length
    ));
  }, [error, selectedRows, selectedColumns])

  useEffect(() => {
    setLoading(isUndefined(columns));
  }, [columns]);

  useEffect(() => {
    setSelectedColumns(pick(selectedData, selectedRows));
  }, [selectedRows, selectedData]);

  const dataTypes = [
    { id: 'adjcategory' },
    { id: 'category' },
    { id: 'currency' },
    { id: 'date' },
    { id: 'datetime' },
    { id: 'datetimestamp' },
    { id: 'float' },
    { id: 'indcategory' },
    { id: 'int' },
    { id: 'intlfloat' },
    { id: 'intlint' },
    { id: 'subcategory' },
    { id: 'text' },
    { id: 'time' }
  ];

  const onDataChange = (id, name, item) => {
    const type = get(item, 'selectedItem.id');
    setSelectedData({
      ...selectedData,
      [id]: { id, name, type, index: id }
    });
  }

  const getSelectedItem = id => {
    const item = selectedColumns[id];
    if (!isEmpty(item)) {
      return { id: item.type };
    }
    return null;
  }

  const getItemToString = (item) => {
    const label = get(item, 'id', '');
    const description = get(item, 'description', '');
    if (label && description) {
      return (
        <div className={`${COMPONENT_NAME}-item-label`}>
          {label}
          <Tooltip direction={'top'} iconDescription={label}>
            <p id='tooltip-body'>
              {description}
            </p>
          </Tooltip>
        </div>
      );
    }
    return label;
  }

  const rows = useMemo(() => {
    return map(columns, (name, index) => {
      const id = `${index}`;
      const isSelectedRow = includes(selectedRows, id);
      return {
        id,
        index,
        name,
        isSelected: isSelectedRow,
        selection: (
          <Dropdown
            disabled={!isSelectedRow}
            invalid={isSelectedRow && !has(selectedColumns, id)}
            hideLabel
            id={`dropdown-${id}`}
            itemToString={item => getItemToString(item)} // get(item, 'id', '')}
            items={DATA_TYPES}
            label={'Choose data type'}
            light
            titleText={'Data Type'}
            selectedItem={getSelectedItem(id)}
            onChange={(item) => onDataChange(index, name, item)}
          />
        )
      }
    });
  }, [columns, selectedRows, selectedColumns]);

  const onSelectionChange = (ids) => {
    if (!isEqual(ids, selectedRows)) {
      setSelectedRows(ids);
    }
  };

  const tableHeaders = [
    {
      key: 'name',
      isSortable: true,
      header: 'Column Name'
    },
    {
      key: 'selection',
      isSortable: false,
      header: 'Data Type'
    }
  ];

  const getEmpty = () => {
    return (
      <EmptyWidget
        heading={'Oops... Something is missing'}
        subText={'No column data found'}
      />
    );
  }

  const mainComponent = () => {

    if (isLoading) {
      return <DataTableSkeleton showHeader={false} showToolbar={false} />
    }

    if (error) {
      return (
        <InlineNotification
          hideCloseButton
          kind={'error'}
          lowContrast
          title={'Oops...'}
          subtitle={error || 'Something went wrong. Try again later.'}
        />
      )
    }

    if (isEmpty(columns)) {
      return getEmpty();
    }

    return (
      <EnhancedDataTable
        id={'column-data-section'}
        headers={tableHeaders}
        hideHeader
        rows={rows}
        onSelectionChange={onSelectionChange}
      />
    );
  }

  return (
    <div className={COMPONENT_NAME}>
      {mainComponent()}
    </div>
  );
}

export default DataSelection;