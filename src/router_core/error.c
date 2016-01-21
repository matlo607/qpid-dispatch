/*
 * Licensed to the Apache Software Foundation (ASF) under one
 * or more contributor license agreements.  See the NOTICE file
 * distributed with this work for additional information
 * regarding copyright ownership.  The ASF licenses this file
 * to you under the Apache License, Version 2.0 (the
 * "License"); you may not use this file except in compliance
 * with the License.  You may obtain a copy of the License at
 * 
 *   http://www.apache.org/licenses/LICENSE-2.0
 * 
 * Unless required by applicable law or agreed to in writing,
 * software distributed under the License is distributed on an
 * "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
 * KIND, either express or implied.  See the License for the
 * specific language governing permissions and limitations
 * under the License.
 */

#include "router_core_private.h"

struct qdr_error_t {
    qdr_field_t *name;
    qdr_field_t *description;
    pn_data_t   *info;
};

ALLOC_DECLARE(qdr_error_t);
ALLOC_DEFINE(qdr_error_t);

qdr_error_t *qdr_error_from_pn(pn_condition_t *pn)
{
    if (!pn)
        return 0;

    qdr_error_t *error = new_qdr_error_t();
    ZERO(error);

    const char *name = pn_condition_get_name(pn);
    if (name && *name)
        error->name = qdr_field(name);

    const char *desc = pn_condition_get_description(pn);
    if (desc && *desc)
        error->description = qdr_field(desc);

    error->info = pn_data(0);

    return error;
}


qdr_error_t *qdr_error(const char *name, const char *description)
{
    qdr_error_t *error = new_qdr_error_t();

    error->name        = qdr_field(name);
    error->description = qdr_field(description);
    error->info        = 0;

    return error;
}


void qdr_error_free(qdr_error_t *error)
{
    if (error == 0)
        return;

    qdr_field_free(error->name);
    qdr_field_free(error->description);
    if (error->info)
        pn_data_free(error->info);

    free_qdr_error_t(error);
}


void qdr_error_copy(qdr_error_t *from, pn_condition_t *to)
{
    if (from->name) {
        unsigned char *name = qd_field_iterator_copy(from->name->iterator);
        pn_condition_set_name(to, (char*) name);
        free(name);
    }

    if (from->description) {
        unsigned char *desc = qd_field_iterator_copy(from->description->iterator);
        pn_condition_set_description(to, (char*) desc);
        free(desc);
    }

    if (from->info)
        pn_data_copy(pn_condition_info(to), from->info);
}

